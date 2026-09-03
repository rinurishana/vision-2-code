# import google.generativeai as genai
# from PIL import Image
#
# # ==== STEP 1: Configure Gemini API ====
# genai.configure(api_key="AIzaSyAR1Mg4QA8WWNYdJDWsa1MPoxcmIpYbSsE")  # Replace with your actual key
#
#
# # ==== STEP 2: Load Image ====
# def load_image(image_path):
#     try:
#         image = Image.open(image_path)
#         return image
#     except Exception as e:
#         print(f"Error loading image: {e}")
#         return None
#
#
# # ==== STEP 3: Get Prescription Text from Gemini ====
# def interpret_image(image, des):
#     try:
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         response = model.generate_content(
#             [
#                 '''Generate pixel-perfect HTML and internal CSS code based on the provided image.
#
# Requirements:
#
# Match layout, spacing, alignment, fonts, colors, and shadows exactly as shown in the image
# Use only HTML5 and internal CSS inside a style tag
# Do not use external CSS or frameworks
# Do not use asterisks anywhere in the code
# Use semantic HTML elements where appropriate
# Include all icons using Font Awesome or inline SVG (whichever best matches the image)
# Ensure responsive structure but prioritize exact desktop layout
# Maintain exact padding, margin, border radius, and color codes from the image
# Use flexbox or grid for layout alignment
# Keep code clean, properly indented, and well structured
# Do not include explanations, only provide the final code,
#  Extract and replicate exact hex color codes and font sizes from the image as closely as possible.''',
#                 # "Generate html code from image with exact design with color and icons full code include internal css. Do not use asterisks (*). Give clean output.",
#                 image
#             ],
#             stream=False
#         )
#         return response.text.replace("*", "")  # Remove asterisks
#     except Exception as e:
#         return f"Gemini API Error: {e}"
#
#
# # ==== MAIN FUNCTION ====
# def generate_code_from_image(image, des):
#     image_path = image  # Change this if needed
#     image = load_image(image_path)
#
#     if image is None:
#         return
#
#     result = interpret_image(image, des)
#
#     print(result)
#     return result
#


import google.generativeai as genai
from PIL import Image

# ==== STEP 1: Configure Gemini API ====
genai.configure(api_key="AQ.Ab8RN6Lt8aOXyf4a2PWeb0AiFQyXNhemV12pcVeoweZEJYSpiw")

# ==== STEP 2: Load Image ====
def load_image(image_path):
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


# ==== STEP 3: Get Prescription Text from Gemini ====
def interpret_image_html(image, des,specification):
    try:
        prompt='''Generate pixel-perfect HTML5 code from the provided image with maximum visual accuracy and exact UI replication.

Critical Objective:

Recreate the uploaded screenshot as closely as possible in HTML and CSS so the final rendered output visually matches the image nearly identically.

Strict Output Rules:

* Return only complete HTML code
* Include all CSS inside a single internal style tag
* Do not return explanations
* Do not return markdown
* Do not return comments
* Do not output anything except valid HTML
* Do not use asterisks anywhere in the generated code

Technology Restrictions:

Use only:

* HTML5
* Internal CSS
* Font Awesome CDN if icons are required
* Inline SVG if needed

Do not use:

* External CSS files
* Tailwind CSS
* Bootstrap
* JavaScript frameworks
* React
* Vue
* Angular

Visual Accuracy Requirements:

Match the image exactly, including:

* Layout structure
* Spacing
* Alignment
* Positioning
* Element proportions
* Container dimensions
* Image aspect ratios
* Visual hierarchy
* Padding
* Margins
* Gaps between elements
* Border radius values
* Border thickness
* Shadows
* Blur intensity
* Opacity
* Transparency
* Overlays
* Gradients
* Elevation
* Layering
* Z-index appearance

Typography Matching:

Replicate typography precisely:

* Font family closest to screenshot
* Font size
* Font weight
* Letter spacing
* Line height
* Text color
* Text alignment
* Text spacing
* Text hierarchy

Color Matching:

* Extract and reproduce exact hex colors from the image
* Match gradients precisely
* Match transparency and overlay colors accurately
* Recreate dark/light surfaces exactly

Modern UI Effects:

If present in the screenshot, recreate accurately:

* Glassmorphism
* Frosted blur
* Neumorphism
* Floating cards
* Soft shadows
* Layered surfaces
* Glow effects
* Transparent panels
* Blurred backgrounds
* Premium dashboard styling

Layout Rules:

* Use Flexbox and CSS Grid appropriately
* Preserve exact spacing relationships
* Maintain exact desktop fidelity
* Ensure clean responsive behavior without changing desktop proportions
* Match section widths and alignments precisely

Component Accuracy:

Recreate all components exactly:

* Navigation bars
* Headers
* Hero sections
* Cards
* Tables
* Buttons
* Inputs
* Search bars
* Sidebars
* Menus
* Avatars
* Badges
* Tags
* Charts
* Image overlays
* Footers

Image Handling:

* Preserve image aspect ratios exactly
* Match image cropping behavior
* Match object-fit appearance
* Match overlays and masks accurately

Code Quality Requirements:

* Use semantic HTML5 structure where appropriate:

  * header
  * nav
  * main
  * section
  * article
  * footer
* Keep DOM hierarchy clean and readable
* Avoid unnecessary wrappers
* Avoid redundant CSS
* Use production-quality formatting and indentation

Rendering Priority:

Prioritize visual similarity over minimal code length and mention image with dummy on code.

The generated HTML should look as close to the original screenshots as possible when rendered in a browser.
  Only return html css code (no explanation).
'''
        if specification!="":
            prompt = '''Generate pixel-perfect HTML5 code from the provided image with maximum visual accuracy and exact UI replication.

            Critical Objective:

            Recreate the uploaded screenshot as closely as possible in HTML and CSS so the final rendered output visually matches the image nearly identically.

            Strict Output Rules:

            * Return only complete HTML code
            * Include all CSS inside a single internal style tag
            * Do not return explanations
            * Do not return markdown
            * Do not return comments
            * Do not output anything except valid HTML
            * Do not use asterisks anywhere in the generated code

            Technology Restrictions:

            Use only:

            * HTML5
            * Internal CSS
            * Font Awesome CDN if icons are required
            * Inline SVG if needed

            Do not use:

            * External CSS files
            * Tailwind CSS
            * Bootstrap
            * JavaScript frameworks
            * React
            * Vue
            * Angular

            Visual Accuracy Requirements:

            Match the image exactly, including:

            * Layout structure
            * Spacing
            * Alignment
            * Positioning
            * Element proportions
            * Container dimensions
            * Image aspect ratios
            * Visual hierarchy
            * Padding
            * Margins
            * Gaps between elements
            * Border radius values
            * Border thickness
            * Shadows
            * Blur intensity
            * Opacity
            * Transparency
            * Overlays
            * Gradients
            * Elevation
            * Layering
            * Z-index appearance

            Typography Matching:

            Replicate typography precisely:

            * Font family closest to screenshot
            * Font size
            * Font weight
            * Letter spacing
            * Line height
            * Text color
            * Text alignment
            * Text spacing
            * Text hierarchy

            Color Matching:

            * Extract and reproduce exact hex colors from the image
            * Match gradients precisely
            * Match transparency and overlay colors accurately
            * Recreate dark/light surfaces exactly

            Modern UI Effects:

            If present in the screenshot, recreate accurately:

            * Glassmorphism
            * Frosted blur
            * Neumorphism
            * Floating cards
            * Soft shadows
            * Layered surfaces
            * Glow effects
            * Transparent panels
            * Blurred backgrounds
            * Premium dashboard styling

            Layout Rules:

            * Use Flexbox and CSS Grid appropriately
            * Preserve exact spacing relationships
            * Maintain exact desktop fidelity
            * Ensure clean responsive behavior without changing desktop proportions
            * Match section widths and alignments precisely

            Component Accuracy:

            Recreate all components exactly:

            * Navigation bars
            * Headers
            * Hero sections
            * Cards
            * Tables
            * Buttons
            * Inputs
            * Search bars
            * Sidebars
            * Menus
            * Avatars
            * Badges
            * Tags
            * Charts
            * Image overlays
            * Footers

            Image Handling:

            * Preserve image aspect ratios exactly
            * Match image cropping behavior
            * Match object-fit appearance
            * Match overlays and masks accurately

            Code Quality Requirements:

            * Use semantic HTML5 structure where appropriate:

              * header
              * nav
              * main
              * section
              * article
              * footer
            * Keep DOM hierarchy clean and readable
            * Avoid unnecessary wrappers
            * Avoid redundant CSS
            * Use production-quality formatting and indentation

            Rendering Priority:

            Prioritize visual similarity over minimal code length and mention image with dummy on code.

            The generated HTML should look as close to the original screenshots as possible when rendered in a browser and add user specification as '''+specification+'''.
              Only return html css code (no explanation).
            '''
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content(
            [

                prompt ,
                image
            ],
            stream=False
        )
        return response.text.replace("*", "")  # Remove asterisks
    except Exception as e:
        return f"Gemini API Error: {e}"

def interpret_image_React(image, des):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content(
            [

                '''

Generate complete React component code with maximum visual accuracy based on the provided image.

Technical Requirements:

* Use React functional components
* Use internal CSS or styled-components only
* Do not use Tailwind CSS
* Do not use Bootstrap
* Do not use external CSS files
* Do not use unnecessary wrappers
* Use semantic structure where appropriate:

  * header
  * nav
  * main
  * section
  * article
  * footer
* Use Flexbox and CSS Grid where needed
* Ensure responsive behavior while prioritizing exact desktop fidelity
* Output only production-quality React code

Visual Accuracy Requirements:

Match the screenshot exactly, including:

* Layout structure
* Alignment
* Spacing
* Padding
* Margins
* Border radius
* Shadows
* Gradients
* Blur effects
* Glassmorphism or neumorphism effects
* Opacity levels
* Overlays
* Borders
* Elevation
* Component sizing
* Exact proportions
* Whitespace hierarchy

Typography Requirements:

Replicate typography precisely:

* Font family
* Font size
* Font weight
* Letter spacing
* Line height
* Text alignment
* Text transformation
* Text color

Color Requirements:

* Extract and reproduce exact hex colors from the image
* Match gradients precisely
* Match transparency and overlays accurately

Component Accuracy:

Recreate all UI components exactly:

* Buttons
* Inputs
* Cards
* Navigation bars
* Sidebars
* Tables
* Avatars
* Modals
* Badges
* Tags
* Charts
* Image overlays

Icons:

Use:

* Font Awesome CDN
  or
* Inline SVG

Choose whichever most closely matches the screenshot.

Code Quality:

* Use clean indentation
* Organize styles clearly
* Keep DOM hierarchy readable
* Avoid redundant styles
* Avoid inline clutter where possible
* Use reusable class naming

Rendering Rules:

* Prioritize visual similarity over shorter code
* Preserve all spacing and alignment exactly
* Preserve image aspect ratios
* Match hover appearance visually if visible in screenshot
* Match shadow softness and blur intensity accurately
* Ensure desktop layout matches pixel-perfect proportions

Output Rules:

* Output only the complete React component code
* Include all CSS within the same file
* Do not include explanations
* Do not include markdown
* Do not include comments
* Do not use asterisks anywhere in the code

If the image contains modern UI effects such as:

* glassmorphism
* frosted blur
* layered shadows
* floating cards
* soft gradients
* translucent panels

recreate them accurately using CSS.

Generate code that visually matches the screenshot as closely as possible, even if the code becomes longer. Only return react code (no explanation).
''',
                image
            ],
            stream=False
        )
        return response.text.replace("*", "")  # Remove asterisks
    except Exception as e:
        return f"Gemini API Error: {e}"

def interpret_image_Flutter(image, des):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        response = model.generate_content(
            [

                '''

Generate complete Flutter UI code with maximum visual accuracy based on the provided image.

Technical Requirements:

* Use Flutter with Dart
* Use StatelessWidget or StatefulWidget appropriately
* Use only Flutter widgets
* Do not use unnecessary packages
* Avoid third-party UI frameworks
* Use clean widget hierarchy
* Use responsive layout techniques while prioritizing exact desktop or mobile fidelity
* Organize code professionally and cleanly
* Output only production-quality Flutter code

Layout Requirements:

Match the screenshot exactly, including:

* Layout structure
* Alignment
* Element positioning
* Spacing
* Padding
* Margins
* Border radius
* Widths and heights
* Aspect ratios
* Visual hierarchy
* Container proportions
* Layering order

Typography Requirements:

Replicate typography precisely:

* Font size
* Font weight
* Letter spacing
* Line height
* Text alignment
* Text colors
* Font family closest to screenshot

Color Requirements:

* Extract and reproduce exact hex color values
* Match gradients precisely
* Match transparency and opacity accurately
* Recreate overlays and tint effects

Effects Requirements:

Recreate all visual effects exactly:

* Shadows
* Elevation
* Blur effects
* Glassmorphism
* Frosted backgrounds
* Neumorphism
* Gradient overlays
* Transparency
* Card elevation
* Soft UI effects

Component Requirements:

Recreate all UI elements exactly:

* App bars
* Navigation bars
* Side menus
* Cards
* Buttons
* Input fields
* Search bars
* Tables
* Avatars
* Tags
* Chips
* Bottom navigation
* Floating action buttons
* Dialogs
* Image overlays
* Scrollable sections

Flutter Widget Usage:

Use appropriate Flutter widgets such as:

* Scaffold
* SafeArea
* Container
* Row
* Column
* Stack
* Positioned
* Expanded
* Flexible
* GridView
* ListView
* CustomScrollView
* ClipRRect
* BackdropFilter
* ShaderMask
* BoxDecoration
* LinearGradient
* RichText

Design Accuracy:

* Match all shadows and blur radii accurately
* Match border thickness and opacity
* Match elevation softness precisely
* Preserve whitespace exactly
* Preserve component scaling and alignment
* Maintain exact spacing between elements
* Recreate layered UI accurately

Responsive Requirements:

* Ensure responsive scaling
* Maintain layout integrity on different screen sizes
* Prioritize exact screenshot fidelity first

Code Quality:

* Use proper widget decomposition if needed
* Keep code readable and production-ready
* Avoid redundant widgets
* Use const constructors where appropriate
* Use proper naming conventions
* Maintain organized indentation

Output Rules:

* Output only complete Flutter code
* Do not include explanations
* Do not include markdown
* Do not include comments
* Do not use asterisks anywhere in the code

If the screenshot contains:

* glassmorphism
* translucent layers
* floating cards
* modern dashboard UI
* soft gradients
* animated-looking layouts
* premium SaaS styling
* blurred overlays

recreate them accurately using Flutter widgets and decoration properties.

Prioritize visual similarity over shorter code length and generate UI that matches the screenshot as closely as possible. Only return flutter - dart code (no explanation).
''',
                image
            ],
            stream=False
        )
        return response.text.replace("*", "")  # Remove asterisks
    except Exception as e:
        return f"Gemini API Error: {e}"


# ==== MAIN FUNCTION ====
def generate_code_from_image(image, des,type,specification):
    image_path = image  # Change this if needed
    image = load_image(image_path)
    print(type,"===========")
    if image is None:
        return
    if type=="html":
        result = interpret_image_html(image, des,specification)

        print(result)
        return result
    elif type=="react":
        result = interpret_image_React(image, des)

        print(result)
        return result

    elif type=="flutter":
        result = interpret_image_Flutter(image, des)

        print(result)
        return result
    return
# print(generate_code_from_image(r"C:\Users\navee\Downloads\vision2code (1)\vision2code\vision2code\gg.jpg","","flutter"))