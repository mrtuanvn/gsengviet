#!/bin/bash
set -e

SPACE_URL="https://huggingface.co/spaces/tuanipad/GSEngViet"
SRC_DIR="./VI-Translate"
TMP_DIR="hf_space_tmp"

rm -rf "$TMP_DIR"
echo "==> Cloning Hugging Face Space repository..."
git clone "$SPACE_URL" "$TMP_DIR"

cd "$TMP_DIR"
echo "==> Initializing Git LFS..."
git lfs install
git lfs track "*.png" "*.ttf" "*.onnx" "*.ico"
git add .gitattributes

echo "==> Copying application files..."
cp -a "../$SRC_DIR/." .

# Remove unnecessary github folder containing logo images
rm -rf .github

echo "==> Renormalizing binary files for Git LFS..."
git add --renormalize .
git add .

echo "==> Committing and pushing to Hugging Face..."
git commit -m "Deploy VI-Translate to Hugging Face Space (Git LFS fixed)" || echo "No changes to commit"
git push

cd ..
rm -rf "$TMP_DIR"
echo "==> Deploy completed successfully!"
