"use client"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { usePerformanceTest } from "@/hooks/use-hotels"
import { Clock, Database, Search, Zap } from "lucide-react"

export function PerformanceTest() {
  const { isRunning, results, error, runPerformanceTest } = usePerformanceTest()

  const handleRunTest = async () => {
    try {
      await runPerformanceTest()
    } catch (err) {
      console.error("Performance test failed:", err)
    }
  }

  return (
    <Card className="mb-8">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Zap className="h-5 w-5 text-primary" />
          Performance Test
        </CardTitle>
        <p className="text-sm text-muted-foreground">Test search performance with large dataset (1M+ hotels)</p>
      </CardHeader>
      <CardContent>
        <div className="flex items-center gap-4 mb-4">
          <Button onClick={handleRunTest} disabled={isRunning} className="bg-primary hover:bg-primary/90">
            {isRunning ? (
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full animate-spin" />
                Running Test...
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Search className="h-4 w-4" />
                Run Performance Test
              </div>
            )}
          </Button>
        </div>

        {error && <div className="text-sm text-destructive mb-4">Error: {error}</div>}

        {results && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-muted p-4 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <Database className="h-4 w-4 text-primary" />
                <span className="text-sm font-medium">Total Hotels</span>
              </div>
              <div className="text-2xl font-bold text-foreground">{results.total_hotels_in_db.toLocaleString()}</div>
            </div>

            <div className="bg-muted p-4 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <Search className="h-4 w-4 text-primary" />
                <span className="text-sm font-medium">Results Found</span>
              </div>
              <div className="text-2xl font-bold text-foreground">{results.results_count.toLocaleString()}</div>
            </div>

            <div className="bg-muted p-4 rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <Clock className="h-4 w-4 text-primary" />
                <span className="text-sm font-medium">Execution Time</span>
              </div>
              <div className="text-2xl font-bold text-foreground">{results.execution_time_ms}ms</div>
              <Badge variant={results.execution_time_ms < 100 ? "default" : "secondary"} className="mt-1">
                {results.execution_time_ms < 50
                  ? "Excellent"
                  : results.execution_time_ms < 100
                    ? "Good"
                    : results.execution_time_ms < 500
                      ? "Fair"
                      : "Slow"}
              </Badge>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
