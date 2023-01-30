from paddleocr.tools.infer.predict_system import main
import subprocess
import paddleocr.tools.infer.utility as utility



if __name__ == "__main__":
    args = utility.parse_args()
    args.image_dir = "D:\\code\\mygit\\PaddleOCR\\test.png"
    args.det_model_dir = "D:\\code\\ggggg\\paddleOcr-server\\whl\\rec\\en\\en_PP-OCRv3_rec_infer"
    args.rec_model_dir ="D:\\code\\ggggg\\paddleOcr-server\\whl\\rec\\en\\en_PP-OCRv3_rec_infer"
    args.rec_char_dict_path = "D:\\code\\ggggg\\paddleOcr-server\\paddleocr\\ppocr\\utils\\en_dict.txt"
    args.draw_img_save_dir = "D:\\code\\ggggg\\paddleOcr-server\\temp"

    main(args)