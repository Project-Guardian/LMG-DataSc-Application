$targetPath = Read-Host -Prompt "Enter path"
Write-Host "---------------------------------------------------------------------";

$List = Get-ChildItem -LiteralPath $targetPath -Directory
ForEach ($Folder in $List) {
    if ($Folder -like '(* *B *) *') {    #'* (* *B)'#!!!!!!!!!!!!!!!!!!!!! missing bracket
        $Matching = $Folder `
        -ireplace '\([0-3] B [a-zA-Z_0-9][a-zA-Z_0-9][a-zA-Z_0-9]\)', "" `
        -ireplace '\([0-3] [A-Z]B [a-zA-Z_0-9][a-zA-Z_0-9][a-zA-Z_0-9]\)', "" `
        -ireplace '\([0-9] [A-Z]B [a-zA-Z_0-9][.][a-zA-Z_0-9][a-zA-Z_0-9]\)', "" `
        -ireplace '\([0-9] [A-Z]B [a-zA-Z_0-9][a-zA-Z_0-9][.][a-zA-Z_0-9]\)', "" `
        -ireplace '\([0-9] [A-Z]B [a-zA-Z_0-9][a-zA-Z_0-9][a-zA-Z_0-9][.]\)', "";
        Write-Host "This folder already has the size and will be rechecked: " $Folder;
        Rename-Item -LiteralPath $Folder.FullName $Matching.Trim();
    }
}
Write-Host "---------------------------------------------------------------------";
Write-Host "Finished removing folder sizes";

Read-Host -Prompt "Completed. Press Enter to exit";