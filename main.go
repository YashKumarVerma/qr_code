package main

import (
	"fmt"
	"image/png"
	"io/ioutil"
	"os"
	"sync"

	"github.com/skip2/go-qrcode"
)

func generateQRCode(data string, filename string, version qrcode.RecoveryLevel) {
	qr, err := qrcode.New(data, version)
	if err != nil {
		fmt.Println("Error generating QR code:", err)
		return
	}

	qr.DisableBorder = true

	file, err := os.Create(filename)
	if err != nil {
		fmt.Println("Error creating file:", err)
		return
	}
	defer file.Close()

	err = png.Encode(file, qr.Image(256))
	if err != nil {
		fmt.Println("Error encoding PNG:", err)
		return
	}

	fmt.Println("QR code generated:", filename)
}

func divideIntoChunks(data string, chunkSize int) []string {
	var chunks []string
	for i := 0; i < len(data); i += chunkSize {
		end := i + chunkSize
		if end > len(data) {
			end = len(data)
		}
		chunks = append(chunks, data[i:end])
	}
	return chunks
}

func readFileAsString(filename string) (string, error) {
	content, err := ioutil.ReadFile(filename)
	if err != nil {
		return "", err
	}
	return string(content), nil
}

func main() {
	filename := "./qr_codes/qr_code_%d.png"
	data, err := readFileAsString("./input.hex")
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}
	chunkSize := 1000

	// Create directory to store QR codes
	err = os.Mkdir("qr_codes", os.ModePerm)
	if err != nil && !os.IsExist(err) {
		fmt.Println("Error creating directory:", err)
		return
	}

	chunks := divideIntoChunks(data, chunkSize)
	var wg sync.WaitGroup
	wg.Add(len(chunks))

	for i, chunk := range chunks {
		qrFilename := fmt.Sprintf(filename, i)
		go func(chunk string, qrFilename string) {
			defer wg.Done()
			generateQRCode(chunk, qrFilename, qrcode.Highest)
		}(chunk, qrFilename)
	}

	wg.Wait()

	fmt.Println("QR codes generated successfully.")
}
