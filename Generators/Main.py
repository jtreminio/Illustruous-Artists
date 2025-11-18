import os

# Paths relative to this script
script_dir = os.path.dirname(__file__)
project_root = os.path.dirname(script_dir)

# Directory containing the images (at project root)
image_dir = os.path.join(project_root, "Images")
artists_txt_path = os.path.join(project_root, "artists.txt")

# HTML template for the main page
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Illustruous-Artists</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #003366; /* Dark blue background */
            color: #d3d3d3; /* White-grey text color */
        }
        .prompt-container {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .prompt {
            padding: 10px;
            border-radius: 5px;
            width: 48%;
            box-sizing: border-box;
        }
        .positive-prompt {
            background-color: #228b22; /* Greenish background */
            color: #ffffff; /* White text color */
        }
        .negative-prompt {
            background-color: #b22222; /* Redish background */
            color: #ffffff; /* White text color */
        }
        .image-container {
            display: flex;
            flex-wrap: wrap;
        }
        .image-item {
            margin: 10px;
            width: 310px; /* Width to accommodate the image and border */
            box-sizing: border-box; /* Ensures padding and border are included in the element's total width and height */
        }
        img {
            max-width: 100%; /* Adjusted to fit within the container */
            height: auto;
            display: block;
            border: 3px solid #003366; /* Invisible border */
            transition: border 0.3s ease-in-out; /* Smooth transition for hover effect */
        }
        img:hover {
            border-color: #fef; /* Purple frame on hover */
        }
        .caption {
            text-align: center;
            margin-top: 5px;
        }
        .caption .artist-name {
            font-weight: bold; /* Bold artist name */
            color: #ffffff; /* White color for artist name */
        }
        .nav-link {
            color: #ffffff;
            margin: 20px 0;
            display: block;
            text-decoration: none;
            font-size: 18px;
        }
        #copy-notification {
            position: fixed;
            bottom: 20px;
            left: 20px;
            background-color: rgba(0, 0, 0, 0.8);
            color: #ffffff;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 14px;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease-in-out;
        }
        #copy-notification.visible {
            opacity: 1;
        }
    </style>
    <script>
        let copyNotificationTimeoutId;

        const showCopyNotification = () => {
            const el = document.getElementById('copy-notification');
            if (!el) return;

            el.classList.add('visible');

            if (copyNotificationTimeoutId) {
                clearTimeout(copyNotificationTimeoutId);
            }

            copyNotificationTimeoutId = setTimeout(() => {
                el.classList.remove('visible');
            }, 1000);
        };

        const copyToClipboard = (text) => {
            navigator.clipboard
                .writeText(`artist ${text}`)
                .then(showCopyNotification)
                .catch(showCopyNotification);
        };
    </script>
</head>
<body>
    <h1>Illustruous Artists</h1>
    <div class="prompt-container">
        <div class="prompt positive-prompt">
            <strong>Positive Prompt:</strong>
            masterpiece, 4k, high quality, artist: Eigaka. 1girl, solo, Sakura, pink short hair, green eyes, forehead protector, blushing, looking at viewer, smiling, white dress, green background, gradient background
        </div>
        <div class="prompt negative-prompt">
            <strong>Negative Prompt:</strong>
            worst quality, low quality, text, censored, blurry, (watermark), artist signature, artist name
        </div>
    </div>
    <div id="copy-notification">Copied!</div>
    <div class="image-container">
        {images}
    </div>
</body>
</html>
"""

# Generate HTML for individual artist images, iterating by artists.txt order
image_html = ""

with open(artists_txt_path, encoding="utf-8") as artists_file:
    for line in artists_file:
        artist_name = line.strip()
        if not artist_name:
            continue

        # Expected filename pattern based on artist name
        filename = f"Artist-{artist_name}_00001_.png"
        image_path = os.path.join(image_dir, filename)

        if not os.path.exists(image_path):
            # Skip artists that don't have a corresponding image file
            continue

        # Escape single quotes for inline JS string
        js_artist_name = artist_name.replace("\\", "\\\\").replace("'", "\\'")

        image_html += f'''
        <div class="image-item">
            <img src="Images/{filename}" alt="{artist_name}" onclick="copyToClipboard('{js_artist_name}')">
            <div class="caption">
                <span class="artist">Artist:</span> <span class="artist-name">{artist_name}</span>
            </div>
        </div>
        '''

# Combine HTML template with images for main page
final_html = html_template.replace("{images}", image_html)

# Save the HTML file for the main page at project root
output_path = os.path.join(project_root, "index.html")
with open(output_path, "w") as file:
    file.write(final_html)

print("index.html have been created")
