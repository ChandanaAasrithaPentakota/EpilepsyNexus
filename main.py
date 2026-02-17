import argparse
from build_graph import build_graph
from graph import EpilepsyState


def main():
    parser = argparse.ArgumentParser(
        description="EpilepsyNexus Multimodal AI"
    )

    parser.add_argument(
        "--mri",
        type=str,
        required=True,
        help="Path to MRI image"
    )

    parser.add_argument(
        "--eeg",
        type=str,
        required=True,
        help="Path to EEG text file"
    )

    parser.add_argument(
        "--symptoms",
        type=str,
        required=True,
        help="Patient symptom description"
    )

    args = parser.parse_args()

    # Build graph
    
    graph = build_graph()

    # Create state
    # 
    state = EpilepsyState(
        mri_image_path=args.mri,
        eeg_text_file_path=args.eeg,
        symptoms_text=args.symptoms
    )

    # Run pipeline
    result = graph.invoke(state)

    print(result)


if __name__ == "__main__":
    main()
