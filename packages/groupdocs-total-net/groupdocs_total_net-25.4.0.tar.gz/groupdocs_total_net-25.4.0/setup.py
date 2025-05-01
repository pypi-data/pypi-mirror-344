from setuptools import setup

NAME = "groupdocs-total-net"
VERSION = "25.4.0"

REQUIRES = ["groupdocs-comparison-net==24.12",
            "groupdocs-conversion-net==24.12",
            "groupdocs-metadata-net==25.4",
            "groupdocs-signature-net==25.4",
            "groupdocs-viewer-net==24.9",
            "groupdocs-watermark-net==25.3"]

"""
REQUIRES = [
            "groupdocs-metadata-net"]
"""

setup(
    name=NAME,
    version=VERSION,
    description='GroupDocs.Total for Python via .NET is an all-in-one suite that provides powerful APIs for document comparison, viewing, and watermarking. This package is designed to enhance your document management capabilities with ease and efficiency, catering to a wide range of file formats and functionalities.',
    keywords = [
    "GroupDocs.Total for Python via .NET", "GroupDocs.Comparison for Python via .NET", "GroupDocs.Viewer for Python via .NET", "GroupDocs.Watermark for Python via .NET", 
    "document comparison", "document viewing", "document watermarking", "compare documents", "view documents", "add watermarks", "remove watermarks", 
    "Python document management", "API", "Microsoft Office", "PDF", "raster images", "TIFF", "JPEG", "GIF", "PNG", "BMP", 
    "line-by-line comparison", "paragraph comparison", "character comparison", "style comparison", "shape comparison", "position comparison", 
    "document rendering", "HTML", "JPG", "PNG", "document formats", "document metadata", "text watermark", "image watermark", 
    "OpenDocument", "DOC", "DOCX", "XLSX", "PPTX", "DWG", "DXF", "PSD", "AI", "CDR", 
    "PDF rasterization", "email attachments", "Office cloud font", "render files", "file information", "document attachments", 
    "watermark search", "watermark removal", "watermark application", "Microsoft Word", "Microsoft Excel", "Microsoft PowerPoint", 
    "Microsoft Visio", "OpenOffice", "Email", "Fixed Layout", "file types", "document types", 
    "Windows", "Linux", "macOS", "Python 3.11 or later", "installation", "pip install", "upgrade package"],
    url='https://products.groupdocs.com/',
    author='GroupDocs',
    author_email='support@groupdocs.com',
    packages=['groupdocs-total-net'],
    include_package_data=True,
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    install_requires=REQUIRES,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: Other/Proprietary License'
    ],
    platforms=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows Vista',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.5',
)
