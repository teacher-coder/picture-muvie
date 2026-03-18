import IconPlus from "../icons/IconPlus";

interface Props {
  onClick: () => void;
}

export default function MergeButton({ onClick }: Props) {
  return (
    <div className="flex items-center gap-2 py-0.5 pl-9">
      <div className="h-px flex-1 bg-border" />
      <button
        onClick={onClick}
        className="flex items-center gap-1 rounded-full border border-border bg-surface px-2.5 py-0.5 text-[11px] font-medium text-text-muted transition-all duration-200 hover:border-primary/30 hover:bg-primary/5 hover:text-primary active:scale-95"
      >
        <IconPlus />
        합치기
      </button>
      <div className="h-px flex-1 bg-border" />
    </div>
  );
}
