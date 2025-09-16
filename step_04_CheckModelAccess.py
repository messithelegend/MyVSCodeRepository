import boto3
import csv

def list_all_bedrock_models(region_name='us-east-1', output_csv='bedrock_model_list.csv'):
    """
    Lists all Bedrock models and writes to CSV safely.
    """
    bedrock = boto3.client("bedrock", region_name=region_name)

    try:
        response = bedrock.list_foundation_models()
        models = []

        print(f"\n🔍 All Bedrock Models in Region: {region_name}\n")

        for model in response['modelSummaries']:
            model_id = model.get('modelId', 'N/A')
            provider = model.get('providerName', 'N/A')
            model_name = model.get('modelName', 'N/A')
            access = model.get('accessType', 'N/A')

            modalities = model.get('outputModalities', [])
            inference_types = model.get('inferenceTypesSupported', [])

            output_modalities_str = ', '.join(modalities) if modalities else 'N/A'
            inference_types_str = ', '.join(inference_types) if inference_types else 'N/A'
            access_mark = "✅" if access == "GRANTED" else "❌"

            print(f"{access_mark} {model_name} ({model_id})")
            print(f"   ↳ Provider: {provider}")
            print(f"   ↳ Output: {output_modalities_str}")
            print(f"   ↳ Inference: {inference_types_str}")
            print(f"   ↳ Access: {access}\n")

            models.append({
                "Model Name": model_name,
                "Model ID": model_id,
                "Provider": provider,
                "Access": access,
                "Output Modalities": output_modalities_str,
                "Inference Types": inference_types_str
            })

        # Write to CSV
        with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=models[0].keys())
            writer.writeheader()
            writer.writerows(models)

        print(f"📄 CSV written to: {output_csv}")

    except Exception as e:
        print(f"\n❌ Error retrieving model list: {e}")

if __name__ == "__main__":
    list_all_bedrock_models(region_name="us-east-1")
