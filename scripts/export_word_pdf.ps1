<#
Export a DOCX working copy through desktop Microsoft Word on Windows.
PDF-only never saves the source DOCX. -DocxPath also delivers the updated copy.
Existing output files are not overwritten. Exit 0 = exported, 1 = field update
or export failure, 2 = input/environment unavailable. Rendering still needs review.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$InputPath,
    [Parameter(Mandatory = $true)][string]$PdfPath,
    [string]$DocxPath,
    [string]$ReportPath
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$word = $null
$document = $null
$workDoc = $null
$workPdf = $null
$originalUpdateLinks = $null
$result = [ordered]@{ schema = 'thesisforge.word-export/1'; status = 'INPUT_ERROR'; visual_review = 'NOT_RUN'; field_errors = @(); outputs = @() }
$exitCode = 2

function Assert-StaticPackage {
    param([string]$Path)
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = [IO.Compression.ZipFile]::OpenRead($Path)
    try {
        $bytes = 0L
        $seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
        foreach ($entry in $archive.Entries) {
            if (-not $seen.Add($entry.FullName)) { throw 'Duplicate ZIP entry.' }
            $bytes += $entry.Length
            if ($bytes -gt 134217728 -or $archive.Entries.Count -gt 10000) { throw 'Package exceeds inspection limits.' }
            if ($entry.FullName -match 'vbaProject') { throw 'VBA payload is unsupported.' }
            if ($entry.FullName -notmatch '^word/.*\.(xml|rels)$') { continue }
            $stream = $entry.Open()
            $reader = $null
            try {
                $settings = New-Object System.Xml.XmlReaderSettings
                $settings.DtdProcessing = [System.Xml.DtdProcessing]::Prohibit
                $settings.XmlResolver = $null
                $reader = [System.Xml.XmlReader]::Create($stream, $settings)
                $xml = New-Object System.Xml.XmlDocument
                $xml.XmlResolver = $null
                $xml.Load($reader)
                foreach ($rel in $xml.SelectNodes('//*[local-name()="Relationship"]')) {
                    if ($rel.GetAttribute('TargetMode') -eq 'External' -and $rel.GetAttribute('Type') -notmatch '/hyperlink$') {
                        throw "External document dependency is unsupported: $($entry.FullName)"
                    }
                }
                $instructions = @($xml.SelectNodes('//*[local-name()="instrText"]') | ForEach-Object { $_.InnerText }) -join ''
                foreach ($node in $xml.SelectNodes('//*[local-name()="fldSimple"]')) {
                    foreach ($attribute in $node.Attributes) {
                        if ($attribute.LocalName -eq 'instr') { $instructions += ' ' + $attribute.Value }
                    }
                }
                if ($instructions -match '\b(DDEAUTO|DDE|INCLUDETEXT|INCLUDEPICTURE|LINK|DATABASE)\b') {
                    throw 'External-data fields require a separately reviewed export workflow.'
                }
            }
            finally {
                if ($reader) { $reader.Dispose() }
                $stream.Dispose()
            }
        }
    }
    finally { $archive.Dispose() }
}

try {
    if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) { throw 'Desktop Word COM requires Windows.' }
    $source = (Resolve-Path -LiteralPath $InputPath).Path
    if ([IO.Path]::GetExtension($source).ToLowerInvariant() -ne '.docx') { throw 'Input must be .docx.' }
    $pdf = [IO.Path]::GetFullPath($PdfPath)
    if ([IO.Path]::GetExtension($pdf).ToLowerInvariant() -ne '.pdf') { throw 'PdfPath must end in .pdf.' }
    $targets = @($pdf)
    $docx = $null
    if ($DocxPath) {
        $docx = [IO.Path]::GetFullPath($DocxPath)
        if ([IO.Path]::GetExtension($docx).ToLowerInvariant() -ne '.docx') { throw 'DocxPath must end in .docx.' }
        $targets += $docx
    }
    if ($ReportPath) { $ReportPath = [IO.Path]::GetFullPath($ReportPath); $targets += $ReportPath }
    if (@($targets | Select-Object -Unique).Count -ne $targets.Count) { throw 'Output paths must be distinct.' }
    foreach ($target in $targets) {
        if ($target -eq $source -or (Test-Path -LiteralPath $target)) { throw "Output already exists or aliases input: $target" }
    }
    Assert-StaticPackage -Path $source
    $result.input = $source
    $result.input_sha256 = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
    foreach ($target in $targets) {
        $null = [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($target))
    }
    $token = [Guid]::NewGuid().ToString('N')
    $workDoc = Join-Path ([IO.Path]::GetDirectoryName($pdf)) ('.thesisforge-word-' + $token + '.docx')
    $workPdf = Join-Path ([IO.Path]::GetDirectoryName($pdf)) ('.thesisforge-word-' + $token + '.pdf')
    [IO.File]::Copy($source, $workDoc, $false)
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $originalUpdateLinks = $word.Options.UpdateLinksAtOpen
    $word.Options.UpdateLinksAtOpen = $false
    $document = $word.Documents.Open($workDoc, $false, $false, $false)
    $exitCode = 1
    $result.status = 'EXPORT_FAILED'
    foreach ($firstRange in $document.StoryRanges) {
        $range = $firstRange
        while ($null -ne $range) {
            try {
                $failedIndex = $range.Fields.Update()
                if ($failedIndex -ne 0) { $result.field_errors += "Field update returned index $failedIndex in story $($range.StoryType)." }
            }
            catch { $result.field_errors += $_.Exception.Message }
            try { $range = $range.NextStoryRange }
            catch { $result.field_errors += 'Could not traverse all story ranges.'; $range = $null }
        }
    }
    foreach ($toc in $document.TablesOfContents) {
        try { $toc.Update(); $toc.UpdatePageNumbers() }
        catch { $result.field_errors += $_.Exception.Message }
    }
    $document.Repaginate()
    # Persist only the isolated working copy when dual-format delivery is asked.
    if ($docx) { $document.Save() }
    $document.ExportAsFixedFormat($workPdf, 17)
    $document.Close([ref]0)
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($document)
    $document = $null
    if (-not (Test-Path -LiteralPath $workPdf) -or (Get-Item -LiteralPath $workPdf).Length -eq 0) { throw 'No PDF produced.' }
    if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant() -ne $result.input_sha256) { throw 'Source changed during export.' }
    [IO.File]::Move($workPdf, $pdf)
    $result.outputs += @{ kind = 'pdf'; path = $pdf; sha256 = (Get-FileHash -LiteralPath $pdf -Algorithm SHA256).Hash.ToLowerInvariant() }
    if ($docx) {
        [IO.File]::Move($workDoc, $docx)
        $result.outputs += @{ kind = 'docx'; path = $docx; sha256 = (Get-FileHash -LiteralPath $docx -Algorithm SHA256).Hash.ToLowerInvariant() }
    }
    $result.source_preserved = $true
    if ($result.field_errors.Count -gt 0) { $result.status = 'EXPORTED_WITH_FIELD_ERRORS'; $exitCode = 1 }
    else { $result.status = 'EXPORTED'; $exitCode = 0 }
}
catch { $result.error = $_.Exception.Message }
finally {
    if ($document) {
        try { $document.Close([ref]0) } catch { $result.cleanup_error = $_.Exception.Message }
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($document)
    }
    if ($word) {
        try {
            if ($null -ne $originalUpdateLinks) { $word.Options.UpdateLinksAtOpen = $originalUpdateLinks }
            $word.Quit()
        } catch { $result.cleanup_error = $_.Exception.Message }
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word)
    }
    foreach ($temporary in @($workDoc, $workPdf)) {
        if ($temporary -and (Test-Path -LiteralPath $temporary)) { Remove-Item -LiteralPath $temporary -Force }
    }
}
$payload = $result | ConvertTo-Json -Depth 8
if ($ReportPath -and -not (Test-Path -LiteralPath $ReportPath)) {
    try {
        $stream = [IO.File]::Open($ReportPath, [IO.FileMode]::CreateNew)
        $writer = New-Object IO.StreamWriter($stream, (New-Object Text.UTF8Encoding($false)))
        try { $writer.WriteLine($payload) } finally { $writer.Dispose() }
    } catch { [Console]::Error.WriteLine($_.Exception.Message); $exitCode = 1 }
}
[Console]::WriteLine($payload)
exit $exitCode
