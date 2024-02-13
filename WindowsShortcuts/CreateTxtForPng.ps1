# Open file dialog to select .png files
Add-Type -AssemblyName System.Windows.Forms
$dialog = New-Object System.Windows.Forms.OpenFileDialog
$dialog.Filter = "PNG images (*.png)|*.png"
$dialog.Multiselect = $true

# Show the dialog and get the result
$result = $dialog.ShowDialog()

# Check if the 'OK' button was pressed
if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
    # Loop through each selected file
    foreach ($file in $dialog.FileNames) {
        # Create a new .txt file with the same name as the .png file
        $newFileName = [System.IO.Path]::ChangeExtension($file, ".txt")
        New-Item -Path $newFileName -ItemType "file" -Force
    }
}
