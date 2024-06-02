"use client";

import React, { useState, useRef } from "react";

import { type editor } from "monaco-editor";
import Editor, { Monaco } from "@monaco-editor/react";
import TestCodeButton from "@/app/_components/test-code-button";
import SubmitButton from "@/app/_components/submit-button";
import CodeOutput from "@/app/_components/code-output";

export default function CodeEditorWrapper() {
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);
  const [output, setOutput] = useState<string>("");

  function handleEditorDidMount(
    editor: editor.IStandaloneCodeEditor | null,
    monaco: Monaco
  ) {
    editorRef.current = editor;
  }

  const handleTestCodeOnClick = async () => {
    if (editorRef.current) {
      const code = editorRef.current.getValue();

      try {
        const response = await fetch("/api/test", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ content: code }),
        });

        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        setOutput(data.output);
      } catch (error) {
        console.error("Error testing code:", error);
        alert(
          "Failed to run the code. Please check the console for more details."
        );
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <nav className="bg-gray-800 shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center flex-grow">
              <span className="text-xl font-bold">CodePython</span>
            </div>
            <div className="flex-1 flex justify-center">
              <TestCodeButton onClick={handleTestCodeOnClick}></TestCodeButton>
            </div>
            <div className="flex items-center">
              <SubmitButton></SubmitButton>
            </div>
          </div>
        </div>
      </nav>
      <div className="flex flex-1 p-6 space-x-4">
        <div className="w-1/2">
          <div className="editor-container">
            <Editor
              height="60vh"
              defaultLanguage="python"
              defaultValue="# Write your Python code here"
              theme="vs-dark"
              onMount={handleEditorDidMount}
            />
          </div>
        </div>
        <CodeOutput output={output} />
      </div>
    </div>
  );
}
