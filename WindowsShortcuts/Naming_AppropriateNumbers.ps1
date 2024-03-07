Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName Microsoft.VisualBasic

# Prompt for starting number
$startNumber = [Microsoft.VisualBasic.Interaction]::InputBox("Enter the starting number (e.g., 01, 001, 0001):", "Starting Number", "01")

# Ensure valid input
if (![string]::IsNullOrWhiteSpace($startNumber) -and $startNumber -match '^\d+$') {
    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Filter = "Image files (*.jpg;*.jpeg;*.png)|*.jpg;*.jpeg;*.png"
    $dialog.Multiselect = $true

    $result = $dialog.ShowDialog()

    if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
        $counter = [int]$startNumber
        $length = $startNumber.Length

        foreach ($file in $dialog.FileNames) {
            $formattedNumber = $counter.ToString("D$length")
            $newFileName = [System.IO.Path]::GetDirectoryName($file) + "\" + $formattedNumber + [System.IO.Path]::GetExtension($file)
            Rename-Item $file -NewName $newFileName
            $counter++
        }
    }
} else {
    [System.Windows.Forms.MessageBox]::Show("Invalid input. Please enter a numeric value.", "Error", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
}
