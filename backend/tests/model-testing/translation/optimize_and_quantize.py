import os
from onnxruntime.quantization import quantize_dynamic, QuantType

def quantize_onnx_model(optimized_model_path, quantized_model_path):
    """Quantize the optimized ONNX model to INT8."""
    quantize_dynamic(
        model_input=optimized_model_path,
        model_output=quantized_model_path,
        weight_type=QuantType.QInt8
    )
    print(f"Quantized model saved to {quantized_model_path}")

def main():
    # Paths to the models - using existing optimized ONNX models
    base_path = "../../../../model_cache/marian_de_onnx_optimized"
    
    # Quantize decoder model
    decoder_model_path = f"{base_path}/decoder_model.onnx"
    decoder_quantized_path = f"{base_path}/decoder_model_quantized.onnx"
    
    # Quantize encoder model
    encoder_model_path = f"{base_path}/encoder_model.onnx"
    encoder_quantized_path = f"{base_path}/encoder_model_quantized.onnx"
    
    # Quantize decoder_with_past model
    decoder_past_model_path = f"{base_path}/decoder_with_past_model.onnx"
    decoder_past_quantized_path = f"{base_path}/decoder_with_past_model_quantized.onnx"
    
    # Quantize all models
    models_to_quantize = [
        (decoder_model_path, decoder_quantized_path, "Decoder"),
        (encoder_model_path, encoder_quantized_path, "Encoder"),
        (decoder_past_model_path, decoder_past_quantized_path, "Decoder with Past")
    ]
    
    for model_path, quantized_path, model_name in models_to_quantize:
        if os.path.exists(model_path):
            print(f"Quantizing {model_name} model...")
            quantize_onnx_model(model_path, quantized_path)
        else:
            print(f"{model_name} model not found at {model_path}")

if __name__ == "__main__":
    main()