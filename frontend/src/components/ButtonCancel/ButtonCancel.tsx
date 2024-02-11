import styles from './ButtonCancel.module.scss';
const ButtonCancel = ({
  text,
  className,
  isDirty,
  isValid,
  onClick
}: {
  text: string;
  className?: string;
  isDirty?: boolean;
  isValid?: boolean;
  onClick?: React.MouseEventHandler<HTMLButtonElement>
}) => {
  return (
    <button
      className={className === 'cancel_style_red' ? `${styles.cancel} ${styles.cancel_style_red}` : `${styles.cancel}`}
      type="button"
      disabled={!isDirty || !isValid}
      onClick={onClick}

    >
      {text}
    </button>
  );
};

export default ButtonCancel;
