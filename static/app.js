const p = document.querySelector("#prompt");
const img = document.querySelector("#result");
const btn = document.querySelector("#generate");
const lvl = document.querySelector("#levelText");
const why = document.querySelector("#explain");
const status = document.querySelector("#status");

function level() {
    let n = 1;
    const t = p.value.toLowerCase();

    [" in ", "style", "lighting", "lens", "depth", "detailed", "cinematic", "3d"]
        .forEach(x => {
            if (t.includes(x)) n++;
        });

    return Math.min(5, n);
}

function refresh() {
    const n = level();
    const t = p.value.toLowerCase();
    const a = ["clear subject"];

    lvl.textContent = n + " / 5";

    if (t.includes(" in ")) a.push("a defined setting");
    if (/style|3d|cinematic/.test(t)) a.push("a visual style");
    if (/lighting|golden/.test(t)) a.push("lighting direction");
    if (/lens|depth|detailed/.test(t)) a.push("camera/detail cues");

    why.textContent =
        "This prompt contains " +
        a.join(", ") +
        ". Each extra constraint gives the image model more information about the intended result.";
}

document.querySelectorAll("[data-add]").forEach(button => {
    button.onclick = () => {
        p.value = p.value.trim() + button.dataset.add;
        refresh();
    };
});

p.oninput = refresh;

btn.onclick = async () => {
    btn.disabled = true;
    btn.textContent = "Generating...";

    try {
        const response = await fetch("/api/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                prompt: p.value,
                level: level() - 1
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Image generation failed.");
        }

        if (!data.image) {
            throw new Error("The server returned no image.");
        }

        console.log("Image received:", data.mode);

        img.onload = () => {
            console.log("Image loaded successfully.");
        };

        img.onerror = () => {
            console.error("The browser could not display the returned image.");
            alert("The image was generated, but the browser could not display it.");
        };

        img.src = data.image;

        status.textContent =
            data.mode === "real" ? "AI image mode" : "Demo mode";

    } catch (error) {
        console.error("Generation error:", error);
        alert(error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = "Generate image";
    }
};

refresh();
