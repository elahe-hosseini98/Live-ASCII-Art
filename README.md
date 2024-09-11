# Live ASCII Art Project

This project captures webcam frames and displays them as ASCII art in real-time. It supports two methods for generating the ASCII art:

1. **Regular Algorithmic Approach**: Converts frames to ASCII art using a traditional algorithm.
2. **AI-Based Approach**: Converts frames to ASCII art using a trained CNN model.

## Project Structure

- `/img_to_ascii`:
  - The real-time ASCII art display logic from the webcam feed.
- `/AI_based_model/`:
  - Contains the model (`model.py`) and the training script for the AI-based ASCII art generator.
- `/data/`:
  - Holds scripts for dataset creation and data loading, including generating ASCII art from images.
- `/app/`:
  - Contains the terminal user interface (`tui.py`) which handles the user interaction when the application is running.
  
## How It Works

When the project is run, it captures frames from your webcam and displays the output as ASCII art in the terminal. You can switch between two modes:
- **Regular Mode**: ASCII art is generated using a predefined algorithm.
- **AI Mode**: ASCII art is generated using a CNN model trained on the CelebA dataset.

### Running the Project

To run the project, simply execute `main.py` from the root directory:

```bash
python main.py
```

### Training the AI Model

For the AI-based approach, we used the **CelebA dataset** with over **200,000 face images**. These images were converted to ASCII art using the algorithmic approach, and the pairs (image, ASCII art) were used to train a **2D CNN model**. The dataset handling and the data loader are located in the `/data` subdirectory.

**Note:** **Due to the large size of the dataset and the trained model, these are not included in this repository. Attempting to switch to the AI mode without these files will result in an error.**

### Sample Output (Regular Mode)

Here is a sample of the ASCII art output from the regular mode:

[Sample Output]![Screenshot (8)](https://github.com/user-attachments/assets/6dad8075-ad2b-4aaa-b763-978d5f43fc09)

