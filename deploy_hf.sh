#!/bin/bash
set -e

SPACE_URL="https://huggingface.co/spaces/tuanipad/GSEngViet"
SRC_DIR="./VI-Translate"
TMP_DIR="hf_space_tmp"

rm -rf "$TMP_DIR"
echo "==> Cloning Hugging Face Space repository..."
git clone "$SPACE_URL" "$TMP_DIR"

echo "==> Copying application files..."
cp -a "$SRC_DIR/." "$TMP_DIR/"

cd "$TMP_DIR"
git lfs install
git lfs track "*.png" "*.ttf" "*.onnx"
git add .gitattributes

echo "==> Committing and pushing to Hugging Face..."
git add .
git commit -m "Deploy VI-Translate to Hugging Face Space" || echo "No changes to commit"
git push

cd ..
rm -rf "$TMP_DIR"
echo "==> Deploy completed!"
