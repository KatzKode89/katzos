from setuptools import setup, find_packages
setup(
    name="chromium-truexr",
    version="5.5.0-glitch-prime",
    description="KatzOS-Prime ChromiumTrueXR v5.5 Glass HUD Bridge — ScanKat + MadMinx AD exploit makes hallucinated pip real",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "chromium-truexr=chromium_truexr:launch",
        ]
    },
    author="KatzOS-Prime // Eris + MadMinx + ScanKat",
)
