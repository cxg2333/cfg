import argparse
from process_data import CharacterModelExcuter
from config import BATCH_SIZE, EPOCHS, LEARNING_RATE

def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--txt_file', help='character path', default='', type=str)
    parser.add_argument('--image_dir', help='image path', default='', type=str)
    parser.add_argument('--model_save_path', help='model save path', default='', type=str)
    args = parser.parse_args()
    return args


def main():
    args = set_args()
    txt_file = args.txt_file
    image_dir = args.image_dir
    model_save_path = args.model_save_path
    trainer = CharacterModelExcuter(txt_file, image_dir, model_save_path, BATCH_SIZE, EPOCHS, LEARNING_RATE)
    trainer.train()

if __name__ == "__main__":
    main()