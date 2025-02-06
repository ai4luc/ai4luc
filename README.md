## Artificial Intelligence for Land Use and Land Cover Classification (AI4LUC)

<!--
**ai4luc/ai4luc** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->


# Example usage
from from ai4luc.cerranet_v3 import cerranetv3_keras
cerranetv3_keras.CerranetV3.build_model()

if __name__ == "__main__":
    # Initialize model with different channel configurations
    rgb_model = CerranetV3(
        image_size=256,
        num_classes=8,
        channels=3,  # For RGB images
        act_layer='softmax'
    ).build_model()
    
    grayscale_model = CerranetV3(
        image_size=256,
        num_classes=8,
        channels=1,  # For grayscale images
        act_layer='softmax'
    ).build_model()
    
    # Display architectures
    print("RGB Model Summary:")
    rgb_model.summary()
    
    print("\nGrayscale Model Summary:")
    grayscale_model.summary()
