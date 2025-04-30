from pyftdi.i2c import I2cController

class I2CShell:
    def __init__(self, device_url: str):
        """Initialize the I2C shell with the given FTDI device URL."""
        self.device_url = device_url
        self.i2c = I2cController()
        self.configure()

    def configure(self):
        """Configure the I2C controller to connect to the FTDI device."""
        self.i2c.configure(self.device_url)
        print("FTDI I2C Interface Ready. Type 'exit' to quit.")

    def run(self):
        """Run the interactive shell for user commands."""
        while True:
            try:
                command = input("> ").strip()
                if command.lower() in ['exit', 'quit', 'q']:
                    break

                parts = command.split()
                if not parts:
                    continue

                cmd_type = parts[0].lower()
                if cmd_type == 'write':
                    self.handle_write(parts)
                elif cmd_type == 'read':
                    self.handle_read(parts)
                else:
                    print("Unknown command. Use 'write' or 'read'.")
            
            except Exception as e:
                print(f"Error: {e}")

    def handle_write(self, parts):
        """Handle the write command."""
        if len(parts) < 4:
            print("Usage: write <device address> <register> <data...>")
            return
        
        dev_addr = int(parts[1], 0)
        reg_addr = int(parts[2], 0)
        data = [int(x, 0) for x in parts[3:]]

        slave = self.i2c.get_port(dev_addr)
        slave.write_to(reg_addr, bytes(data))

    def handle_read(self, parts):
        """Handle the read command."""
        if len(parts) != 4:
            print("Usage: read <device address> <register> <length>")
            return
        
        dev_addr = int(parts[1], 0)
        reg_addr = int(parts[2], 0)
        length = int(parts[3], 0)

        slave = self.i2c.get_port(dev_addr)
        data = slave.read_from(reg_addr, length)

        # Format read data as hex values for pretty print
        hex_data = [f"0x{byte:02X}" for byte in data]
        print(f"Read: {hex_data}")
