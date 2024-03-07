Add-Type -AssemblyName System.Windows.Forms
$dialog = New-Object System.Windows.Forms.OpenFileDialog
$dialog.Filter = "Image files (*.jpg;*.jpeg;*.png)|*.jpg;*.jpeg;*.png"
$dialog.Multiselect = $true

$result = $dialog.ShowDialog()

if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
    $random = New-Object System.Random
    $usedNumbers = @()
    foreach ($file in $dialog.FileNames) {
        do {
            $randomNumber = $random.Next(100, 1000) # Generate a random 3-digit number
        }
        while ($usedNumbers -contains $randomNumber)
        $usedNumbers += $randomNumber

        $newFileName = [System.IO.Path]::GetDirectoryName($file) + "\" + $randomNumber.ToString() + [System.IO.Path]::GetExtension($file)
        Rename-Item $file -NewName $newFileName
    }
}
