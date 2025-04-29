import argparse
import json
import logging
import pathlib
from datetime import timedelta
from typing import Iterator, Optional

import grpc
import soundfile as sf
from google.protobuf.duration_pb2 import Duration
from phonexia.grpc.common.core_pb2 import Audio, RawAudioConfig, TimeRange
from phonexia.grpc.technologies.denoiser.v1.denoiser_pb2 import DenoiseRequest, DenoiseResponse
from phonexia.grpc.technologies.denoiser.v1.denoiser_pb2_grpc import DenoiserStub


def time_to_duration(time: float) -> Optional[Duration]:
    if time is None:
        return None
    duration = Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def make_request(
    file: str,
    start: Optional[float],
    end: Optional[float],
    use_raw_audio: bool,
) -> Iterator[DenoiseRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    chunk_size = 1024 * 100
    if use_raw_audio:
        with sf.SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )
            for data in r.blocks(blocksize=r.samplerate, dtype="int16"):
                yield DenoiseRequest(
                    audio=Audio(
                        content=data.flatten().tobytes(),
                        raw_audio_config=raw_audio_config,
                        time_range=time_range,
                    )
                )
                time_range = None
                raw_audio_config = None

    else:
        with open(file, mode="rb") as fd:
            while chunk := fd.read(chunk_size):
                yield DenoiseRequest(audio=Audio(content=chunk, time_range=time_range))
                time_range = None


def write_result(
    audio_path: str,
    output_file: pathlib.Path,
    billed_time: timedelta,
    audio_data: bytearray,
    raw_audio_config: Optional[RawAudioConfig] = None,
) -> None:
    logging.info(f"Writing denoised audio to '{output_file}'")
    if raw_audio_config is None:
        with open(output_file, "wb") as f:
            f.write(audio_data)
    else:
        with sf.SoundFile(
            output_file,
            mode="w",
            samplerate=raw_audio_config.sample_rate_hertz,
            channels=1,
            subtype="PCM_16",
            format="wav",
        ) as file:
            file.buffer_write(audio_data, dtype="int16")

    result = {
        "audio": audio_path,
        "total_billed_time": str(billed_time),
        "file_path": str(output_file),
    }
    print(json.dumps(result, indent=2))


def denoise(
    channel: grpc.Channel,
    file: str,
    output_file: pathlib.Path,
    start: Optional[float],
    end: Optional[float],
    metadata: Optional[list],
    use_raw_audio: bool,
) -> None:
    logging.info(f"Denoising '{file}'")
    stub = DenoiserStub(channel)
    response_it: Iterator[DenoiseResponse] = stub.Denoise(
        make_request(file, start, end, use_raw_audio),
        metadata=metadata,
    )
    billed_time = timedelta()
    audio_data = bytearray()
    raw_audio_config = None
    for response in response_it:
        if response.HasField("processed_audio_length"):
            billed_time = response.processed_audio_length.ToTimedelta()
        if response.result.audio.HasField("raw_audio_config"):
            raw_audio_config = response.result.audio.raw_audio_config
        audio_data += response.result.audio.content

    write_result(file, output_file, billed_time, audio_data, raw_audio_config)


def existing_file(file: str) -> str:
    if not pathlib.Path(file).exists():
        raise argparse.ArgumentError(argument=None, message=f"File {file} does not exist")
    return file


def main():
    parser = argparse.ArgumentParser(
        description="Denoiser gRPC client. Removing noises and other disturbing elements from audio recordings."
    )
    parser.add_argument(
        "-H",
        "--host",
        type=str,
        default="localhost:8080",
        help="Server address, default: localhost:8080",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        type=str,
        default="error",
        choices=["critical", "error", "warning", "info", "debug"],
    )
    parser.add_argument(
        "--metadata",
        metavar="key=value",
        nargs="+",
        type=lambda x: tuple(x.split("=")),
        help="Custom client metadata",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        required=True,
        help="Output audio file in 'wav' format. The samplerate will be the same as of the input file",
    )

    parser.add_argument("--use_ssl", action="store_true", help="Use SSL connection")
    parser.add_argument("--start", type=float, help="Audio start time")
    parser.add_argument("--end", type=float, help="Audio end time")
    parser.add_argument(
        "--use_raw_audio", action="store_true", help="Send the input in a raw format"
    )
    parser.add_argument("file", type=existing_file, help="Input audio file")

    args = parser.parse_args()

    if args.start is not None and args.start < 0:
        raise ValueError("Parameter 'start' must be a non-negative float.")

    if args.end is not None and args.end <= 0:
        raise ValueError("Parameter 'end' must be a positive float.")

    if args.start is not None and args.end is not None and args.start >= args.end:
        raise ValueError("Parameter 'end' must be larger than 'start'.")

    logging.basicConfig(
        level=args.log_level.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        logging.info(f"Connecting to {args.host}")
        if args.use_ssl:
            with grpc.secure_channel(
                target=args.host, credentials=grpc.ssl_channel_credentials()
            ) as channel:
                denoise(
                    channel=channel,
                    file=args.file,
                    output_file=args.output,
                    start=args.start,
                    end=args.end,
                    metadata=args.metadata,
                    use_raw_audio=args.use_raw_audio,
                )
        else:
            with grpc.insecure_channel(target=args.host) as channel:
                denoise(
                    channel=channel,
                    file=args.file,
                    output_file=args.output,
                    start=args.start,
                    end=args.end,
                    metadata=args.metadata,
                    use_raw_audio=args.use_raw_audio,
                )

    except grpc.RpcError as e:
        logging.exception(f"RPC failed: {e}")  # noqa: TRY401
        exit(1)
    except Exception:
        logging.exception("Unknown error")
        exit(1)


if __name__ == "__main__":
    main()
