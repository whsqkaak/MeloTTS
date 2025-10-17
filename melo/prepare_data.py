"""
오디오 데이터 디렉터리를 입력받아
`metadata.list`를 작성하는 코드

데이터는 AIHUB의 kaist-audio-book을 사용하는 것으로 가정

"""

import argparse
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--source-dir",
        type=str,
        required=True,
        help="Path to audio directory",
    )

    parser.add_argument(
        "--label-dir",
        type=str,
        required=True,
        help="Path to label directory",
    )

    parser.add_argument(
        "--metadata-path",
        type=str,
        default="data/metadata.list",
        help="To save metadata list file",
    )

    parser.add_argument(
        "--language", "-l",
        type=str,
        default="KR",
        help="Language of audio data"
    )
    return parser.parse_args()


def read_kab_csv(
    csv_dir: str
):
    """
    kab(kaist-audio-book) 라벨 데이터인 csv 파일들을 읽어서
    카테고리를 키로 갖고 라벨 텍스트 리스트를 값으로 갖는 딕셔너리 반환
    """
    csv_dir = Path(csv_dir)
    csv_files = sorted(list(csv_dir.rglob('*.csv')))

    result_dict = {}
    for csv_file in csv_files:
        category = csv_file.stem

        with open(csv_file, 'r') as f:
            lines = f.readlines()
            lines = [line.split(',', maxsplit=1)[1].strip() for line in lines]
            lines = [line.replace('"', '').replace("'", "") for line in lines]
        
        result_dict[category] = lines

    return result_dict




def main():
    args = get_args()

    src_dir = Path(args.source_dir)
    label_dir = Path(args.label_dir)
    language = args.language
    metadata_path = Path(args.metadata_path)

    metadatas = []

    # 1. Find Wavs
    print(f"1. Find wavs: {src_dir}...")
    wav_files = sorted(list(src_dir.rglob('*.wav')))

    # 2. Read labels
    print(f"2. Read label files: {label_dir}")
    label_dict = read_kab_csv(label_dir)

    # 3. Make metadata line
    # metadata line eg: <file-path>|<speaker-name>|<language>|<transcript>
    metadatas = []
    print(f"3. Make metadata file...")
    for wav_file in wav_files:
        file_path = str(wav_file)
        speaker_name = f"{language}-test"
        
        category = wav_file.parent.stem
        transcript = label_dict[category][int(wav_file.stem)]

        metadata = f"{file_path}|{speaker_name}|{language}|{transcript}"
        # print(f"Audio: {wav_file}")
        # print(f"transcript: {metadata}")
        # print("-" * 100 + '\n')
        metadatas.append(metadata)


    print(f"4. Write metadata.list: {metadata_path}")
    with open(metadata_path, "w") as f:
        f.write('\n'.join(metadatas))


if __name__ == "__main__":
    main()
