 
# Get the files which should be moved, without folders
$files = Get-ChildItem '' -Recurse | where {!$_.PsIsContainer} ###################################################################EDIT HERE

# List Files which will be moved
$files
 
# Target Filder where files should be moved to. The script will automatically create a folder for the year and month.
$targetPath = '' ###################################################################EDIT HERE
 
foreach ($file in $files)
{
# Get year and Month of the file
# I used LastWriteTime since this are synced files and the creation day will be the date when it was synced
$year = $file.LastWriteTime.Year.ToString()
$month = $file.LastWriteTime.Month.ToString('00')
 
# Out FileName, year and month
$file.Name
$year
$month
 
# Set Directory Path
$Directory = $targetPath + "\" + $year + "\" + $year + ' ' + $month
# Create directory if it doesn't exsist
if (!(Test-Path $Directory))
{
New-Item $directory -type directory
}
 
# Move File to new location
$file | Move-Item -Destination $Directory
}