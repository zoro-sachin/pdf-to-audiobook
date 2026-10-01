# 📖 PDF to Audiobook

A simple desktop application that converts **PDF documents into WAV audiobooks** using Python.

The application extracts selectable text from a PDF and converts it into speech using your computer's text-to-speech engine. It provides a clean Tkinter interface with adjustable speaking speed and background processing.

---

## ✨ Features

- 📄 Select a PDF document
- 🔊 Convert PDF text into speech
- 🎧 Generate audiobook in **WAV format**
- ⚡ Adjustable speaking rate from **120–240 words per minute**
- 🖥️ Clean desktop GUI using Tkinter
- 📊 Conversion progress indicator
- 🔄 Background conversion using threading
- ⚠️ Error handling and validation
- 🔐 No cloud upload required
- 💾 Automatically suggests a `.wav` output filename
- 📝 Displays page and character count after conversion

The application specifically requires selectable text in the PDF; scanned PDFs require OCR before conversion.

---

## 🖥️ Application

The application provides three main sections:

### 1. Source PDF

Select the PDF that you want to convert.

### 2. Save Audio

Choose where the generated WAV audiobook should be saved.

### 3. Speaking Rate

Adjust the speech speed between:

```text
120 WPM ───────── 240 WPM
```

The default speaking rate is:

```text
175 WPM
```



---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Tkinter | Desktop GUI |
| PyPDF2 | PDF text extraction |
| pyttsx3 | Text-to-speech conversion |
| threading | Background conversion |
| queue | Communication between worker and GUI |

---

## 📁 Project Structure

```text
pdf-to-audiobook/
│
├── main.py
└── README.md
```

### `main.py`

Contains the complete PDF-to-audiobook application, including PDF extraction, text-to-speech conversion, GUI, progress handling, and validation.

---

## ⚙️ Requirements

You need:

- Python 3.x
- Tkinter
- PyPDF2
- pyttsx3

Install the required Python packages with:

```bash
pip install PyPDF2 pyttsx3
```

> Tkinter is normally included with standard Python installations.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/pdf-to-audiobook.git
```

### 2. Open the project

```bash
cd pdf-to-audiobook
```

### 3. Install dependencies

```bash
pip install PyPDF2 pyttsx3
```

### 4. Run the application

```bash
python main.py
```

On some systems:

```bash
python3 main.py
```

---

## 🎯 How to Use

### Step 1 — Select a PDF

Click:

```text
Browse
```

and select the PDF you want to convert.

The application automatically suggests a WAV file with the same base filename.

### Step 2 — Choose Output

Click:

```text
Choose
```

and select where you want to save the audiobook.

The output format is automatically set to:

```text
.wav
```



### Step 3 — Adjust Speaking Rate

Use the speaking-rate slider.

Available range:

```text
120 - 240 WPM
```

Default:

```text
175 WPM
```

### Step 4 — Create Audiobook

Click:

```text
Create audiobook
```

The application will:

```text
PDF
 ↓
Extract Text
 ↓
Convert Text to Speech
 ↓
Generate WAV
 ↓
Save Audiobook
```

---

## 🔄 How It Works

The application follows this process:

```text
        Select PDF
            │
            ▼
     Validate PDF
            │
            ▼
     Extract PDF Text
            │
            ▼
      Validate Text
            │
            ▼
    Initialize TTS Engine
            │
            ▼
      Generate WAV
            │
            ▼
      Save Audio File
            │
            ▼
     Audiobook Ready
```

PDF text is extracted using `PdfReader`, and each page's selectable text is combined before being passed to the speech engine.

---

## 🔊 Text-to-Speech

The application uses **pyttsx3** for text-to-speech conversion.

The selected speaking rate is passed to the speech engine before generating the WAV file.

The generated audio is saved as:

```text
WAV
```

---

## ⚡ Background Processing

PDF conversion can take time for large documents.

To keep the interface responsive, the application performs the conversion in a background thread.

The GUI displays:

```text
Reading PDF text…
```

followed by:

```text
Generating audio…
```

and finally:

```text
Finished: filename.wav
```

---

## 📊 Conversion Result

After successful conversion, the application displays:

- Output filename
- Number of PDF pages
- Number of extracted characters

For example:

```text
Audiobook ready

Saved book.wav

25 pages · 84,532 characters
```



---

## ⚠️ Limitations

### Scanned PDFs

The current application works with **selectable PDF text**.

If the PDF contains scanned images instead of selectable text, conversion will fail with a message indicating that OCR is required.

### Output Format

The current implementation generates:

```text
.wav
```

It does not currently provide MP3, M4A, or other audio formats.

### Voice Selection

The current interface provides a speaking-rate control but does not expose a voice-selection option.

---

## 🔐 Privacy

The application processes the PDF locally through the installed Python libraries and speech engine.

There is no cloud upload functionality implemented in the current application.

---

## 🔮 Future Improvements

Possible future versions could include:

- 🎙️ Voice selection
- 🌍 Multiple language support
- 🗣️ Multiple speech engines
- 🎧 MP3 export
- 📑 Chapter detection
- ⏯️ Audio preview and playback
- ⏸️ Pause/resume conversion
- 📊 Determinate conversion progress
- 🔤 OCR support for scanned PDFs
- 📚 Batch PDF conversion
- 🌙 Dark mode
- 📝 Text preview before conversion
- ✂️ Select specific pages
- 🔊 Volume control
- 🎛️ Pitch control
- 📱 Mobile version

---

## 🤝 Contributing

Contributions are welcome.

### 1. Fork the repository

```bash
git fork
```

### 2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

### 3. Make your changes

### 4. Test the application

```bash
python main.py
```

### 5. Commit your changes

```bash
git commit -m "Add new feature"
```

### 6. Push your branch

```bash
git push origin feature/new-feature
```

### 7. Create a Pull Request

---

## 🐛 Error Handling

The application handles several common problems, including:

- PDF file does not exist
- Output location is missing
- PDF and output file are the same
- Password-protected PDF
- PDF contains no selectable text
- Output folder no longer exists
- Speech engine fails to generate audio

The GUI displays appropriate warning or error messages when these situations occur.

---

## 📄 License

No license is currently specified for this project.

If you plan to publish this project as open source, consider adding an appropriate license.

---

## 👨‍💻 Author

**Your Name**

GitHub:

```text
https://github.com/zoro-sachin/pdf-to-audiobook
```

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📌 Project Summary

**PDF to Audiobook** is a lightweight Python desktop application that transforms selectable PDF text into a WAV audiobook using local text-to-speech functionality.

```text
📄 PDF
   ↓
📖 Text Extraction
   ↓
🔊 Text-to-Speech
   ↓
🎧 WAV Audiobook
```
