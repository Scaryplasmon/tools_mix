Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$dialog = New-Object System.Windows.Forms.OpenFileDialog
$dialog.Filter = "Image files (*.jpg;*.jpeg)|*.jpg;*.jpeg"
$dialog.Multiselect = $true

$result = $dialog.ShowDialog()

if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
    foreach ($file in $dialog.FileNames) {
        $img = [System.Drawing.Image]::FromFile($file)
        $newFileName = [System.IO.Path]::ChangeExtension($file, ".png")
        $img.Save($newFileName, [System.Drawing.Imaging.ImageFormat]::Png)
        $img.Dispose()
    }
}
