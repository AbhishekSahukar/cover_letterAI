export const generateLetter = async (formData) => {
  const res = await fetch("/generate", {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Server error");
  return res.json();
};

export const getHistory = async () => {
  const res = await fetch("/history");
  if (!res.ok) return [];
  return res.json();
};

export const downloadPDF = async (letter) => {
  const res = await fetch("/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ letter }),
  });

  if (!res.ok) throw new Error("Failed to generate PDF");

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "cover_letter.pdf";
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
};