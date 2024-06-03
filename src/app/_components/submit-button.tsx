interface SubmitButtonProps {
  onClick: () => void;
}

export default function SubmitButton({ onClick }: SubmitButtonProps) {
  return (
    <button
      onClick={onClick}
      className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
    >
      Submit
    </button>
  );
}
