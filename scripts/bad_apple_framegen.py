"""Simple script to encode frames for the bad apple example"""

import cv2

# pylint: disable=no-member

filepath = input("File path: ")
cap = cv2.VideoCapture(filepath)
output = []

LAST_FRAME = None
SIZE = (12, 9)


def compress(pixels):
    """Compress the changes into position-color pairs."""
    result = []
    for position, color in pixels:
        result.append(
            f"{position:03}{color}"
        )  # Position with 4 digits, followed by the color value (0-9)
    return result


C = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    C += 1
    if C % 30 != 0:
        continue

    # Resize frame
    resized = cv2.resize(frame, SIZE, interpolation=cv2.INTER_NEAREST)

    # Convert to grayscale and normalize to 10 levels (0-9)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    quantized = (gray // 26).astype(int)  # Divide 0-255 into 10 levels (26 per level)

    if LAST_FRAME is not None:
        # Calculate the difference between frames
        diff = quantized != LAST_FRAME
        changed_pixels = []

        # For each pixel that changed, add its position and new color value
        for i, changed in enumerate(diff.flatten()):
            if changed:
                changed_pixels.append((i, quantized.flatten()[i]))

        if changed_pixels:
            # Compress changes into position-color pairs
            encoded = compress(changed_pixels)
            output.append("".join(encoded))
        else:
            output.append("")  # No changes

    # Set the current frame as the last frame
    LAST_FRAME = quantized

# Save output to file with frame separators
with open("output.txt", "w", encoding="utf8") as f:
    f.write("#".join(output))
