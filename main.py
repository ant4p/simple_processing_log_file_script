from parser_file import create_parser
from reports import average_report
from display_reports import average_tabulate

def main():
    parser = create_parser()
    args = parser.parse_args()

    print(f"Input files: {args.file}")
    print(f"Input report: {args.report}")
    print(f"Input data: {args.date}")
    print()

    if args.report == "average":
        stats = average_report(args.file, args.date)
        report = average_tabulate(stats)
        print(report)
    else:
        print("Введите отчёт который хотите увидеть, на данный момент доступен: average")


if __name__ == "__main__":
    main()
