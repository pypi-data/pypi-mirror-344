import argparse
import mywatering.temperature as temperature
import mywatering.watering as watering


def measure_temperature(args: dict) -> None:
    temperature.main(args)


def water_plants(args: dict) -> None:
    watering.main(args)


def main() -> None:
    parser = argparse.ArgumentParser(description="MyWatering client")
    subparsers = parser.add_subparsers(title="Subcommands")

    # measure_temperature
    parser_temp = subparsers.add_parser(
        "temperature", help="Measure temperature and humidity."
    )
    parser_temp.add_argument(
        "-s", "--server", type=str, help="Server host", required=True
    )
    parser_temp.add_argument(
        "-c", "--client-number", type=str, help="Client number", required=True
    )
    parser_temp.add_argument("-u", "--user", type=str, help="Username", required=True)
    parser_temp.add_argument(
        "-p", "--password", type=str, help="Password", required=True
    )
    parser_temp.set_defaults(func=measure_temperature)

    # water_plants
    parser_water = subparsers.add_parser("water", help="Water plants.")
    parser_water.add_argument(
        "-s", "--server", type=str, help="Server host", required=True
    )
    parser_water.add_argument(
        "-c", "--client-number", type=str, help="Client number", required=True
    )
    parser_water.add_argument("-u", "--user", type=str, help="Username", required=True)
    parser_water.add_argument(
        "-p", "--password", type=str, help="Password", required=True
    )
    parser_water.set_defaults(func=water_plants)

    args = parser.parse_args()
    if "func" in args:
        args.func(args)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
