/**
 * Copyright 2023 Adobe
 * All Rights Reserved.
 *
 * NOTICE: Adobe permits you to use, modify, and distribute this file in
 * accordance with the terms of the Adobe license agreement accompanying
 * it.
 */

// gather all the elements we need
const gallery = document.querySelector(".gallery");
const popup = document.querySelector(".popup");
const title = popup.querySelector(".title");
const signer = popup.querySelector(".signer");
const time = popup.querySelector(".time");
const producer = popup.querySelector(".producer");

// Function to upload a file
async function uploadFile(file, name) {
    const formData = new FormData();
    formData.append('file', file, name);

    const response = await fetch(`http://localhost:8000/upload`, {
        method: 'POST',
        body: formData,
    });

    return await response.json();
}

// Add an image to the gallery
function addGalleryItem(data) {
    const galleryItem = document.createElement('div');
    galleryItem.classList.add('container');

    var img = document.createElement('img');
    img.src = data.url;
    img.classList.add("image");
    galleryItem.appendChild(img);

    const badge = document.createElement('img');
    badge.src = "badge.svg";
    badge.classList.add("badge");
    galleryItem.appendChild(badge);

    gallery.appendChild(galleryItem);

    // add popup event listeners
    badge.addEventListener("mouseenter", function() {
        const rect = badge.getBoundingClientRect();

        const report = data.report;

        // Check if report and manifests are defined
        if (report && report.manifests && report.active_manifest !== undefined) {
            // get the active manifest
            const manifest = report.manifests[report.active_manifest];

            console.log("Manifest:", manifest);

            // show the title of the manifest, or the name of the image
            const title = document.querySelector(".title");
            title.textContent = manifest.title || data.name;

            // show the issuer and time of the signature
            const signer = document.querySelector(".signer");
            const issuer = manifest.signature_info?.issuer || "";
            signer.innerHTML = `Signed By: ${issuer}`;

            const time = document.querySelector(".time");
            const sign_time = manifest.signature_info?.time;
            // convert ISO-8601 sign_time to local time
            const date = sign_time ? new Date(sign_time).toLocaleString() : "";
            time.innerHTML = sign_time ? `Signed On: ${date}` : "";

            // truncate the claim generator at first space for first token
            // and then replace underscores and forward slash with spaces
            const generator = manifest.claim_generator?.split(" ")[0].replace(/[_/]/g, " ");
            console.log("Generator:", generator);

            producer.innerHTML = `Produced With: ${generator}`;

            // Position the popup and show it
            popup.style.display = "block";
            popup.style.position = "absolute"; // Ensure the position is absolute
            popup.style.top = `${rect.top + window.scrollY}px`;
            popup.style.left = `${rect.left}px`; // Adjust the left position as needed
        } else {
            console.log("Manifest or report is undefined.");
        }
    });

    badge.addEventListener("mouseleave", function() {
        // hide the popup
        const popup = document.querySelector(".popup");
        popup.style.display = "none";
    });
}

 
// Example of directly sending files from change event (without using a form)
document.getElementById('files').addEventListener('change', (event) => {
    // reset the container
    gallery.innerHTML = "";

    // upload all the selected files to sign, and show the modified images
    for (const file of event.target.files) {
        const formData = new FormData();
        formData.append('file', file, file.name);

        fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
		// Parse the report string into a JSON object
                data.report = JSON.parse(data.report);

		console.log("Data from server:", data); // Check the data being received from the server
		addGalleryItem(data);
	})
        .catch(error => console.error('Error:', error));
    }
});
