interface CodeOutputProps {
  output: string;
}

export default function CodeOutput({ output }: CodeOutputProps) {
  return (
    <div className="w-1/2 bg-gray-800 p-4 rounded-md shadow-md">
      {/* <h2 className="text-lg font-medium text-white">Output:</h2> */}
      <pre>{output}</pre>
    </div>
  );
}
