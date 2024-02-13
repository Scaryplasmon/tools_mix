# Prompt for text input
Add-Type -AssemblyName Microsoft.VisualBasic
$textToAppend = [Microsoft.VisualBasic.Interaction]::InputBox("Enter the text you want to append:", "Append Text to File", "")

# Check if the input is not empty
if (![string]::IsNullOrWhiteSpace($textToAppend)) {
    # Open file dialog to select .txt files
    Add-Type -AssemblyName System.Windows.Forms
    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Filter = "Text files (*.txt)|*.txt"
    $dialog.Multiselect = $true

    # Show the dialog and get the result
    $result = $dialog.ShowDialog()

    # Check if the 'OK' button was pressed
    if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
        # Loop through each selected file
        foreach ($file in $dialog.FileNames) {
            # Append input text to the file
            Add-Content $file $textToAppend
        }
    }
} else {
    [System.Windows.Forms.MessageBox]::Show("No text was entered. Operation canceled.", "Info", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
}
