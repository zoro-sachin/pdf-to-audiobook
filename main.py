import os
import queue
import tempfile
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import pyttsx3
from PyPDF2 import PdfReader


BACKGROUND = "#f2f4ef"
SURFACE = "#ffffff"
INK = "#202820"
MUTED = "#657064"
GREEN = "#38684a"
GREEN_DARK = "#285239"


def extract_pdf_text(pdf_path):
	reader = PdfReader(str(pdf_path))
	if reader.is_encrypted:
		raise ValueError("This PDF is password-protected. Unlock it before converting.")

	pages = [page.extract_text() or "" for page in reader.pages]
	text = "\n\n".join(page.strip() for page in pages if page.strip())
	if not text:
		raise ValueError("No selectable text was found. Scanned PDFs need OCR before conversion.")
	return text, len(pages)


def save_audio(text, output_path, rate):
	output_path = Path(output_path)
	if not output_path.parent.is_dir():
		raise ValueError("The selected output folder no longer exists.")

	temporary_file = tempfile.NamedTemporaryFile(
		prefix=".pdf_audiobook_",
		suffix=".wav",
		dir=output_path.parent,
		delete=False,
	)
	temporary_path = Path(temporary_file.name)
	temporary_file.close()
	temporary_path.unlink()

	engine = None
	try:
		engine = pyttsx3.init()
		engine.setProperty("rate", rate)
		engine.save_to_file(text, str(temporary_path))
		engine.runAndWait()
		engine.stop()
		engine = None
		if not temporary_path.is_file() or temporary_path.stat().st_size == 0:
			raise RuntimeError("The speech engine did not create an audio file.")
		os.replace(temporary_path, output_path)
	finally:
		if engine is not None:
			engine.stop()
		if temporary_path.exists():
			temporary_path.unlink()


class AudiobookApp:
	def __init__(self, root):
		self.root = root
		self.root.title("PDF to Audiobook")
		self.root.geometry("720x540")
		self.root.minsize(600, 500)
		self.root.configure(background=BACKGROUND)

		self.messages = queue.Queue()
		self.pdf_path = tk.StringVar()
		self.output_path = tk.StringVar()
		self.rate = tk.IntVar(value=175)
		self.status = tk.StringVar(value="Choose a PDF to get started.")
		self.busy = False

		self._configure_styles()
		self._build_ui()
		self.root.protocol("WM_DELETE_WINDOW", self._close)
		self.root.after(100, self._poll_messages)

	def _configure_styles(self):
		style = ttk.Style(self.root)
		style.theme_use("clam")
		style.configure("TFrame", background=BACKGROUND)
		style.configure("Card.TFrame", background=SURFACE)
		style.configure("TLabel", background=BACKGROUND, foreground=INK, font=("Segoe UI", 10))
		style.configure("Muted.TLabel", foreground=MUTED, font=("Segoe UI", 9))
		style.configure("Card.TLabel", background=SURFACE, foreground=INK)
		style.configure("Eyebrow.TLabel", foreground=GREEN, font=("Segoe UI", 9, "bold"))
		style.configure("Title.TLabel", font=("Georgia", 27), foreground=INK)
		style.configure("TButton", font=("Segoe UI", 10), padding=(12, 8))
		style.configure("Action.TButton", background=GREEN, foreground="white", font=("Segoe UI", 10, "bold"), padding=(18, 11))
		style.map("Action.TButton", background=[("active", GREEN_DARK), ("disabled", "#9eafa2")])
		style.configure("TEntry", padding=9, fieldbackground="#fbfcfa")
		style.configure("Horizontal.TScale", background=SURFACE)
		style.configure("Horizontal.TProgressbar", troughcolor="#e4e9e2", background=GREEN)

	def _build_ui(self):
		page = ttk.Frame(self.root, padding=(32, 28, 32, 24))
		page.pack(fill="both", expand=True)

		ttk.Label(page, text="LISTENING DESK  /  01", style="Eyebrow.TLabel").pack(anchor="w")
		ttk.Label(page, text="PDF to audiobook", style="Title.TLabel").pack(anchor="w", pady=(5, 2))
		ttk.Label(page, text="Create a WAV audiobook with your computer's built-in voice.", style="Muted.TLabel").pack(anchor="w")

		card = ttk.Frame(page, style="Card.TFrame", padding=22)
		card.pack(fill="x", pady=(26, 18))
		ttk.Label(card, text="SOURCE PDF", style="Eyebrow.TLabel").pack(anchor="w", pady=(0, 9))
		self._file_row(card, self.pdf_path, "Browse", self._choose_pdf)
		ttk.Label(
			card,
			text="Selectable text is required. Scanned pages need OCR before conversion.",
			style="Muted.TLabel",
			wraplength=600,
		).pack(anchor="w", pady=(8, 20))

		ttk.Label(card, text="SAVE AUDIO AS", style="Eyebrow.TLabel").pack(anchor="w", pady=(0, 9))
		self._file_row(card, self.output_path, "Choose", self._choose_output)

		settings = ttk.Frame(page, style="Card.TFrame", padding=22)
		settings.pack(fill="x")
		ttk.Label(settings, text="SPEAKING RATE", style="Eyebrow.TLabel").pack(anchor="w")
		rate_row = ttk.Frame(settings, style="Card.TFrame")
		rate_row.pack(fill="x", pady=(10, 0))
		ttk.Scale(rate_row, from_=120, to=240, variable=self.rate, orient="horizontal").pack(side="left", fill="x", expand=True)
		self.rate_label = ttk.Label(rate_row, text="175 wpm", style="Card.TLabel", width=9, anchor="e")
		self.rate_label.pack(side="right", padx=(14, 0))
		self.rate.trace_add("write", self._update_rate_label)

		footer = ttk.Frame(page)
		footer.pack(fill="x", side="bottom", pady=(20, 0))
		self.convert_button = ttk.Button(footer, text="Create audiobook", style="Action.TButton", command=self._start)
		self.convert_button.pack(side="right")
		self.progress = ttk.Progressbar(footer, mode="indeterminate", length=150)
		self.progress.pack(side="right", padx=(0, 14), pady=(0, 2))
		ttk.Label(footer, textvariable=self.status, style="Muted.TLabel", wraplength=330).pack(side="left", fill="x", expand=True, padx=(0, 12))

	def _file_row(self, parent, variable, button_text, command):
		row = ttk.Frame(parent, style="Card.TFrame")
		row.pack(fill="x")
		ttk.Entry(row, textvariable=variable, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
		ttk.Button(row, text=button_text, command=command).pack(side="right")

	def _choose_pdf(self):
		selected = filedialog.askopenfilename(
			title="Choose a PDF",
			filetypes=(("PDF documents", "*.pdf"),),
		)
		if selected:
			pdf_path = Path(selected)
			self.pdf_path.set(str(pdf_path))
			if not self.output_path.get():
				self.output_path.set(str(pdf_path.with_suffix(".wav")))
			self.status.set(f"Selected {pdf_path.name}")

	def _choose_output(self):
		current = self.output_path.get()
		selected = filedialog.asksaveasfilename(
			title="Save audiobook",
			defaultextension=".wav",
			initialfile=Path(current).name if current else "audiobook.wav",
			filetypes=(("WAV audio", "*.wav"),),
		)
		if selected:
			self.output_path.set(str(Path(selected).with_suffix(".wav")))

	def _update_rate_label(self, *_):
		self.rate_label.configure(text=f"{self.rate.get()} wpm")

	def _start(self):
		pdf_path = Path(self.pdf_path.get()) if self.pdf_path.get() else None
		output_path = Path(self.output_path.get()) if self.output_path.get() else None
		if not pdf_path or not pdf_path.is_file():
			messagebox.showwarning("Choose a PDF", "Select an existing PDF document first.", parent=self.root)
			return
		if not output_path:
			messagebox.showwarning("Choose an output", "Choose where to save the audiobook.", parent=self.root)
			return

		output_path = output_path.with_suffix(".wav")
		if pdf_path.resolve() == output_path.resolve():
			messagebox.showwarning("Choose another output", "The audio file must be different from the PDF.", parent=self.root)
			return

		self.output_path.set(str(output_path))
		self.busy = True
		self.convert_button.configure(state="disabled")
		self.progress.start(12)
		self.status.set("Reading PDF text…")
		threading.Thread(target=self._convert, args=(pdf_path, output_path, self.rate.get()), daemon=True).start()

	def _convert(self, pdf_path, output_path, rate):
		try:
			text, page_count = extract_pdf_text(pdf_path)
			self.messages.put(("status", "Generating audio…"))
			save_audio(text, output_path, rate)
			self.messages.put(("done", (output_path, page_count, len(text))))
		except Exception as error:
			self.messages.put(("error", str(error)))

	def _poll_messages(self):
		try:
			while True:
				kind, payload = self.messages.get_nowait()
				if kind == "status":
					self.status.set(payload)
				elif kind == "done":
					output_path, page_count, character_count = payload
					self.busy = False
					self.progress.stop()
					self.convert_button.configure(state="normal")
					self.status.set(f"Finished: {output_path.name}")
					messagebox.showinfo(
						"Audiobook ready",
						f"Saved {output_path}\n\n{page_count} pages · {character_count:,} characters",
						parent=self.root,
					)
				elif kind == "error":
					self.busy = False
					self.progress.stop()
					self.convert_button.configure(state="normal")
					self.status.set("Conversion could not be completed.")
					messagebox.showerror("Conversion failed", payload, parent=self.root)
		except queue.Empty:
			pass
		self.root.after(100, self._poll_messages)

	def _close(self):
		if self.busy and not messagebox.askyesno(
			"Conversion in progress",
			"Close the app while audio is being created?",
			parent=self.root,
		):
			return
		self.root.destroy()


def main():
	root = tk.Tk()
	AudiobookApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()

