import subprocess
def exif(img):
    import subprocess

def exif(img):
    com = r'C:\Program Files\EXIFTOOL\exiftool'
    command = [com, img]
    
    try:
        # Using subprocess.run() for better control and exception handling
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        
        # Check for any errors
        if result.stderr:
            return f"Error: {result.stderr.strip()}"
        
        output = result.stdout.strip()
        if not output:
            return "No output from ExifTool"
        
        # Parse the output into a dictionary
        data = {}
        for line in output.splitlines():
            if ':' in line:  # Checking if ':' exists to avoid any format issues
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
                
        return data

    except subprocess.TimeoutExpired:
        return "Process killed due to timeout"
    except FileNotFoundError:
        return "ExifTool not found. Please check the path."
    except Exception as e:
        return f"Error: {e}"

# Example usage:
result = exif('C:\\Users\\Saray\\OneDrive\\Desktop\\MINI PROJECT2\\static\\IMG_3172_1.jpg')
#print(result)
latitude = result['GPS Latitude']
longitude = result['GPS Longitude']
print(latitude," ",longitude)
