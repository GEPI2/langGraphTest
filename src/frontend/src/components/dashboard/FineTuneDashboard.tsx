import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { BrainCircuit, Play, RefreshCw } from 'lucide-react';

const FineTuneDashboard = () => {
  const [jobs, setJobs] = useState<any[]>([]);
  const [modelName, setModelName] = useState('gpt2'); // Default small model for testing

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      const res = await fetch('http://localhost:8001/finetune/jobs');
      const data = await res.json();
      setJobs(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleCreateJob = async () => {
    try {
      await fetch('http://localhost:8001/finetune/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          base_model: modelName,
          dataset_path: "data/dataset.jsonl", // Placeholder
          epochs: 1
        }),
      });
      alert('Job created!');
      fetchJobs();
    } catch (err) {
      console.error(err);
      alert('Failed to create job');
    }
  };

  return (
    <div className="p-8 space-y-8 h-full overflow-auto">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Fine-tuning Studio</h2>
        <p className="text-muted-foreground">Train and adapt models to your specific needs.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Create Job */}
        <Card>
          <CardHeader>
            <CardTitle>Start New Training Job</CardTitle>
            <CardDescription>Configure your fine-tuning parameters.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Base Model</label>
              <Input 
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
                placeholder="e.g., gpt2, llama-2-7b"
              />
            </div>
            <Button className="w-full" onClick={handleCreateJob}>
              <Play className="w-4 h-4 mr-2" />
              Start Training
            </Button>
          </CardContent>
        </Card>

        {/* Job List */}
        <Card className="md:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Training Jobs</CardTitle>
              <CardDescription>Monitor your active and past jobs.</CardDescription>
            </div>
            <Button variant="outline" size="icon" onClick={fetchJobs}>
              <RefreshCw className="w-4 h-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {jobs.map((job) => (
                <div key={job.job_id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-4">
                    <div className="p-2 bg-primary/10 rounded-full">
                      <BrainCircuit className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <div className="font-bold">{job.job_id}</div>
                      <div className="text-sm text-muted-foreground">Model: {job.config.base_model}</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className={`px-2 py-1 rounded text-xs font-bold ${
                      job.status === 'completed' ? 'bg-green-100 text-green-700' :
                      job.status === 'running' ? 'bg-blue-100 text-blue-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {job.status.toUpperCase()}
                    </div>
                  </div>
                </div>
              ))}
              {jobs.length === 0 && (
                <div className="text-center text-muted-foreground py-8">
                  No training jobs found.
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default FineTuneDashboard;
