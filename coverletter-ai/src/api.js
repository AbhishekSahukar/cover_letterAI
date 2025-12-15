export const generateLetter = async (formData) => {
  const res = await fetch("http://localhost:8000/generate", {
    method: "POST",
    body: formData,
  });
  return res.json();
};

export const getHistory = async () => {
  const res = await fetch("http://localhost:8000/history");
  return res.json();
};

export const downloadPDF = async (letter) => {
  const res = await fetch("http://localhost:8000/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ letter }),
  });

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "cover_letter.pdf";
  document.body.appendChild(a);
  a.click();

  a.remove();
  window.URL.revokeObjectURL(url);
};

