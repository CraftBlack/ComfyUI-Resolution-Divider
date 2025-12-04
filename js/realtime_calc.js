import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "ResolutionUtils.Divider.Realtime",
    async nodeCreated(node, app) {
        // Ensure this script only runs on our specific node
        if (node.comfyClass !== "ResolutionDividerNode") return;

        // --- 1. FIND WIDGETS ---
        const imgWidget = node.widgets.find(w => w.name === "image");
        const resWidget = node.widgets.find(w => w.name === "res_string");
        const divWidget = node.widgets.find(w => w.name === "divider");

        // --- 2. CREATE LIVE RESULT WIDGET ---
        // This is purely for display purposes
        const displayWidget = node.addWidget("text", "Live Result", "Waiting for Input...", () => {}, {
            multiline: false,
        });

        // Styling the display widget
        if (displayWidget.inputEl) {
            displayWidget.inputEl.readOnly = true;
            displayWidget.inputEl.style.opacity = "0.8";
            displayWidget.inputEl.style.textAlign = "center";
            displayWidget.inputEl.style.backgroundColor = "#222";
            displayWidget.inputEl.style.color = "#0f0"; // Matrix Green
            displayWidget.inputEl.style.marginBottom = "5px";
            displayWidget.inputEl.style.border = "1px solid #444";
        }

        // --- 3. UI LAYOUT (SAFE REORDERING) ---
        // Current order in ComfyUI memory: [res_string, divider, image, Live Result]
        // Target order: [res_string, divider, Live Result, image]
        
        // Find index positions
        const imgIndex = node.widgets.indexOf(imgWidget);
        const displayIndex = node.widgets.indexOf(displayWidget);

        if (imgIndex !== -1 && displayIndex !== -1) {
            // Remove 'Live Result' from the bottom
            node.widgets.splice(displayIndex, 1);
            
            // Insert 'Live Result' BEFORE 'image'
            // This keeps the 'upload button' attached to the image widget safe
            node.widgets.splice(imgIndex, 0, displayWidget);
        }

        // Force node resize to fit new layout
        node.setSize([node.size[0], node.computeSize()[1]]);

        // -----------------------------------------------------------------

        // --- HELPER FUNCTIONS ---

        function updateResolutionFromImage() {
            const filename = imgWidget.value;
            if (!filename) return;
            
            // Fetch image from ComfyUI backend
            const route = `/view?filename=${encodeURIComponent(filename)}&type=input`;
            
            const img = new Image();
            img.onload = function() {
                // Auto-fill the resolution string
                resWidget.value = `${this.naturalWidth} x ${this.naturalHeight}`;
                calculateLive();
            };
            img.src = route;
        }

        function calculateLive() {
            const text = resWidget.value;
            const div = divWidget.value || 1.0;

            if (!text || text.trim() === "") {
                displayWidget.value = "---";
                return;
            }

            // Regex to handle various formats (e.g., "1920x1080", "1920, 1080")
            const cleanStr = text.replace(/[xX*,]/g, " ");
            const parts = cleanStr.match(/\d+/g);

            if (!parts || parts.length < 2) {
                displayWidget.value = "Invalid Format";
                return;
            }

            const w = parseInt(parts[0]);
            const h = parseInt(parts[1]);
            
            // The Math
            const newW = Math.floor(w / div);
            const newH = Math.floor(h / div);

            displayWidget.value = `${newW} x ${newH}`;
        }

        // --- CALLBACKS CHAINING ---
        // Hook into existing widgets to trigger updates
        
        const originalCallbackImg = imgWidget.callback;
        imgWidget.callback = function() {
            if (originalCallbackImg) originalCallbackImg.apply(this, arguments);
            updateResolutionFromImage();
        };

        const originalCallbackRes = resWidget.callback;
        resWidget.callback = function() {
            if (originalCallbackRes) originalCallbackRes.apply(this, arguments);
            calculateLive();
        };

        const originalCallbackDiv = divWidget.callback;
        divWidget.callback = function() {
            if (originalCallbackDiv) originalCallbackDiv.apply(this, arguments);
            calculateLive();
        };

        // --- INITIALIZATION ---
        // Delay slightly to ensure widgets are fully loaded
        setTimeout(() => {
             if (imgWidget.value && (!resWidget.value || resWidget.value === "")) {
                updateResolutionFromImage();
            } else {
                calculateLive();
            }
        }, 100);
    }
});