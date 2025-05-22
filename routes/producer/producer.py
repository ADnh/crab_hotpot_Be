import torch
from transformers import AutoTokenizer
from routes.models.CNN import CNN

# Load tokenizer
phoBertTokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base')

# Thiết lập thiết bị
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Tham số mô hình
EMBEDDING_DIM = 768
N_FILTERS = 32
FILTER_SIZES = [1, 2, 3, 5]
OUTPUT_DIM = 3
DROPOUT = 0.1
PAD_IDX = phoBertTokenizer.pad_token_id

# Khởi tạo mô hình CNN
cnn = CNN(EMBEDDING_DIM, N_FILTERS, FILTER_SIZES, OUTPUT_DIM, DROPOUT, PAD_IDX)

# Load mô hình đã huấn luyện
phoBert = torch.load('./routes/nlp_models/models/phobert_cnn_model_part1_task2a_2.pt', map_location=device)
cnn.load_state_dict(torch.load('./routes/nlp_models/models_state_dict/phobert_cnn_model_part2_task2a_2_state_dict.pt', map_location=device))

# Đặt mô hình ở chế độ đánh giá
phoBert.eval()
cnn.eval()
cnn.to(device)

########################################## Speech to text ##########################3
from transformer import pipeline
file_path = "/home/hoadinh/SpeechToText/crab_hotpot_Be-main/VIVOSDEV01_R044.wav"
output_crack = file_path
def speech_to_text(file_path):
    """
    Args:
        - file_path: path to audio file.
    Returns:
        - vi_sentence: return vietnames sentence
    """
    transcriber = pipeline("automatic-speech-recognition", model="vinai/PhoWhisper-large", device="cuda")
    vi_sentence = transcriber(file_path)
    return vi_sentence

######################################################################################

def predict_class_from_text(processed_sentence):
    """
    Nhận đầu vào là 1 sentence tiếng Việt, trả về lớp dự đoán và xác suất tương ứng.
    """
    # Tokenize câu nhập vào
    phobert_inputs = phoBertTokenizer(processed_sentence, return_tensors="pt")
    phobert_inputs = {key: value.to(device) for key, value in phobert_inputs.items()}

    with torch.no_grad():
        embedded = phoBert(phobert_inputs['input_ids'], phobert_inputs['attention_mask'])[0]
        if embedded.shape[1] < max(FILTER_SIZES):
            raise ValueError("Câu quá ngắn. Vui lòng nhập câu dài hơn để phân tích.")

        predictions = cnn(embedded)

    probabilities = torch.nn.functional.softmax(predictions, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()

    if predicted_class == 0:
        predicted_class = "Không có yếu tố phản động."
    elif predicted_class == 1:
        predicted_class = "Có yếu tố phản động."
    elif predicted_class == 2:
        predicted_class = "Trung lập."

    return predicted_class, probabilities.cpu().numpy()


###
