document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("uploadForm");
    const result = document.getElementById("runId");
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      result.textContent = "Uploading...";
  
      const formData = new FormData(form);
      try {
        const resp = await fetch("/upload", {
          method: "POST",
          body: formData
        });
        if (!resp.ok) {
          throw new Error(`Upload failed: ${resp.statusText}`);
        }
        const data = await resp.json();
        result.textContent = `Run ID: ${data.run_id}`;
      } catch (err) {
        result.textContent = `Error: ${err.message}`;
      }
    });
  });
  