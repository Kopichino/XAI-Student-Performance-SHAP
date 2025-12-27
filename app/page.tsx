"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { AlertCircle, CheckCircle2, TrendingUp } from "lucide-react";

export default function AcademicRiskDashboard() {
  const [g1, setG1] = useState(10);
  const [absences, setAbsences] = useState(5);
  const [studytime, setStudytime] = useState(2);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<{
    risk_score: number;
    label: string;
    shap_image_base64: string;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const analyzeRisk = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          G1: g1,
          absences: absences,
          studytime: studytime,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to analyze risk");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const riskPercentage = result ? Math.round(result.risk_score * 100) : 0;
  const isHighRisk = riskPercentage > 50;

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar/Input Panel */}
      <aside className="w-80 bg-white border-r border-gray-200 p-6 flex flex-col">
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-1">
            Student Parameters
          </h2>
          <p className="text-sm text-gray-500">Adjust values to analyze risk</p>
        </div>

        <div className="space-y-8 flex-1">
          {/* First Period Grade Slider */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-700">
                First Period Grade (G1)
              </label>
              <span className="text-sm font-semibold text-blue-600 bg-blue-50 px-2 py-1 rounded">
                {g1}
              </span>
            </div>
            <Slider
              value={[g1]}
              onValueChange={(value) => setG1(value[0])}
              min={0}
              max={20}
              step={1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>0</span>
              <span>20</span>
            </div>
          </div>

          {/* Absences Slider */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-700">
                Absences
              </label>
              <span className="text-sm font-semibold text-blue-600 bg-blue-50 px-2 py-1 rounded">
                {absences}
              </span>
            </div>
            <Slider
              value={[absences]}
              onValueChange={(value) => setAbsences(value[0])}
              min={0}
              max={93}
              step={1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>0</span>
              <span>93</span>
            </div>
          </div>

          {/* Study Time Slider */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-700">
                Study Time
              </label>
              <span className="text-sm font-semibold text-blue-600 bg-blue-50 px-2 py-1 rounded">
                {studytime}
              </span>
            </div>
            <Slider
              value={[studytime]}
              onValueChange={(value) => setStudytime(value[0])}
              min={1}
              max={4}
              step={1}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>1</span>
              <span>4</span>
            </div>
          </div>
        </div>

        <Button
          onClick={analyzeRisk}
          disabled={isLoading}
          className="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white"
        >
          {isLoading ? (
            <span className="flex items-center gap-2">
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Analyzing...
            </span>
          ) : (
            <span className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Analyze Risk
            </span>
          )}
        </Button>
      </aside>

      {/* Main Dashboard Area */}
      <main className="flex-1 p-8">
        <div className="max-w-5xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Academic Risk Analysis
            </h1>
            <p className="text-gray-600">
              Predictive insights for student dropout risk assessment
            </p>
          </div>

          {error && (
            <Card className="mb-6 border-red-200 bg-red-50">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 text-red-800">
                  <AlertCircle className="w-5 h-5" />
                  <p className="font-medium">{error}</p>
                </div>
              </CardContent>
            </Card>
          )}

          {result ? (
            <div className="space-y-6">
              {/* Risk Score Card */}
              <Card
                className={`border-2 ${
                  isHighRisk
                    ? "border-red-200 bg-red-50"
                    : "border-green-200 bg-green-50"
                }`}
              >
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-gray-900">
                    {isHighRisk ? (
                      <AlertCircle className="w-6 h-6 text-red-600" />
                    ) : (
                      <CheckCircle2 className="w-6 h-6 text-green-600" />
                    )}
                    Risk Assessment
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-6">
                    <div className="flex-1">
                      <div
                        className={`text-6xl font-bold mb-2 ${
                          isHighRisk ? "text-red-600" : "text-green-600"
                        }`}
                      >
                        {riskPercentage}%
                      </div>
                      <div
                        className={`text-lg font-semibold ${
                          isHighRisk ? "text-red-700" : "text-green-700"
                        }`}
                      >
                        {result.label}
                      </div>
                      <p className="text-sm text-gray-600 mt-2">
                        {isHighRisk
                          ? "Student shows elevated risk factors for academic dropout. Intervention recommended."
                          : "Student demonstrates positive indicators for academic success."}
                      </p>
                    </div>
                    <div className="w-32 h-32 flex items-center justify-center">
                      <div className="relative w-full h-full">
                        <svg
                          className="w-full h-full -rotate-90"
                          viewBox="0 0 100 100"
                        >
                          <circle
                            cx="50"
                            cy="50"
                            r="40"
                            fill="none"
                            stroke={isHighRisk ? "#fee2e2" : "#dcfce7"}
                            strokeWidth="8"
                          />
                          <circle
                            cx="50"
                            cy="50"
                            r="40"
                            fill="none"
                            stroke={isHighRisk ? "#dc2626" : "#16a34a"}
                            strokeWidth="8"
                            strokeDasharray={`${riskPercentage * 2.51} 251`}
                            strokeLinecap="round"
                          />
                        </svg>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* SHAP Explanation */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-gray-900">
                    AI Logic (SHAP Explanation)
                  </CardTitle>
                  <CardDescription>
                    Feature importance visualization showing how each parameter
                    influences the risk prediction
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {result.shap_image_base64 ? (
                    <div className="bg-white rounded-lg border border-gray-200 p-4">
                      <img
                        src={`data:image/png;base64,${result.shap_image_base64}`}
                        alt="SHAP Explanation Plot"
                        className="w-full h-auto"
                      />
                    </div>
                  ) : (
                    <p className="text-gray-500 text-center py-8">
                      No explanation image available
                    </p>
                  )}
                </CardContent>
              </Card>
            </div>
          ) : (
            <Card className="border-dashed">
              <CardContent className="pt-12 pb-12 text-center">
                <TrendingUp className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  No Analysis Yet
                </h3>
                <p className="text-gray-500">
                  Adjust the student parameters in the sidebar and click
                  "Analyze Risk" to generate predictions.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </main>
    </div>
  );
}
