import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Search, FileText } from 'lucide-react';

const RAGDashboard = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8001/rag/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      alert(`Uploaded: ${data.filename} (${data.chunks_added} chunks)`);
    } catch (err) {
      console.error(err);
      alert('Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  const handleSearch = async () => {
    if (!query) return;
    try {
      const res = await fetch(`http://localhost:8001/rag/query?query=${encodeURIComponent(query)}&n_results=5`, {
        method: 'POST',
      });
      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
      alert('Search failed');
    }
  };

  return (
    <div className="p-8 space-y-8 h-full overflow-auto">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">RAG Knowledge Base</h2>
        <p className="text-muted-foreground">Manage documents and test retrieval.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Upload Section */}
        <Card>
          <CardHeader>
            <CardTitle>Upload Document</CardTitle>
            <CardDescription>Supported formats: .txt, .pdf</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              <Input type="file" onChange={handleUpload} disabled={isUploading} />
              {isUploading && <span className="text-sm text-muted-foreground">Uploading...</span>}
            </div>
          </CardContent>
        </Card>

        {/* Search Section */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Test Retrieval</CardTitle>
            <CardDescription>Search through your knowledge base.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex gap-2">
              <Input 
                placeholder="Enter your query..." 
                value={query} 
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              />
              <Button onClick={handleSearch}>
                <Search className="w-4 h-4 mr-2" />
                Search
              </Button>
            </div>

            <div className="space-y-2">
              {results.map((result, idx) => (
                <div key={idx} className="p-4 border rounded-lg bg-muted/50">
                  <p className="text-sm mb-2">{result.content}</p>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <FileText className="w-3 h-3" />
                    <span>Distance: {result.distance?.toFixed(4)}</span>
                  </div>
                </div>
              ))}
              {results.length === 0 && query && (
                <div className="text-center text-muted-foreground py-8">
                  No results found.
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default RAGDashboard;
