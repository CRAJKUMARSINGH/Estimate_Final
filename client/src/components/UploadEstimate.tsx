import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, FileSpreadsheet, X } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export function UploadEstimate() {
  const [file, setFile] = useState<File | null>(null);
  const { toast } = useToast();

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      console.log('File uploaded:', acceptedFiles[0].name);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
    },
    maxFiles: 1,
  });

  const handleUpload = () => {
    if (file) {
      console.log('Processing file:', file.name);
      toast({
        title: "File uploaded",
        description: `${file.name} has been uploaded successfully.`,
      });
    }
  };

  const removeFile = () => {
    setFile(null);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Estimate</CardTitle>
        <CardDescription>Upload an Excel file to create a new estimate</CardDescription>
      </CardHeader>
      <CardContent>
        {!file ? (
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-md p-8 text-center cursor-pointer hover-elevate ${
              isDragActive ? 'border-primary bg-accent' : 'border-border'
            }`}
            data-testid="dropzone-upload"
          >
            <input {...getInputProps()} data-testid="input-file" />
            <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
            <p className="text-sm font-medium mb-2">
              {isDragActive ? 'Drop the file here' : 'Drag & drop an Excel file here'}
            </p>
            <p className="text-sm text-muted-foreground mb-4">or</p>
            <Button type="button" variant="secondary" data-testid="button-browse">
              Browse Files
            </Button>
            <p className="text-xs text-muted-foreground mt-4">
              Supported formats: .xlsx, .xls
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center gap-4 p-4 border rounded-md">
              <FileSpreadsheet className="h-8 w-8 text-primary" />
              <div className="flex-1">
                <p className="font-medium text-sm" data-testid="text-filename">{file.name}</p>
                <p className="text-xs text-muted-foreground">
                  {(file.size / 1024).toFixed(2)} KB
                </p>
              </div>
              <Button
                variant="ghost"
                size="icon"
                onClick={removeFile}
                data-testid="button-remove-file"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <Button onClick={handleUpload} className="w-full" data-testid="button-upload">
              Process Estimate
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
