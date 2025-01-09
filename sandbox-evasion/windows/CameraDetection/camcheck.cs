using Windows.Media.Capture;
using Windows.Storage;
using Windows.Devices.Enumeration;

namespace DefaultNamespace;

public class camcheck
{
    public void main()
    {
        check1();
        check2();
    }
    public void check1()
    {
        CameraCaptureUI captureUI = new CameraCaptureUI();
        captureUI.PhotoSettings.Format = CameraCaptureUIPhotoFormat.Jpeg;
        StorageFile photo = await captureUI.CaptureFileAsync(CameraCaptureUIMode.Photo);

        if (photo == null)
        {
            Console.WriteLine("[-] camera not detected.");
            return;
        }
        else
        {
            Console.WriteLine("[+] camera detected!");
            
        }

        return;

    }

    public void check2()
    {
        bool isthere = enumDev();

        if (isthere)
        {
            Console.WriteLine("[-] camera not detected.");
        }
        else
        {
            Console.WriteLine("[+] camera detected!");

        }


    }
    async bool enumDev(){
        DeviceInformationCollection devCol = await DeviceInformation.FindAllAsync();
        
        foreach(DeviceInformation dev in devCol)
        {

            if (dev.Name == Regex.IsMatch(input, @".*cam.*", RegexOptions.IgnoreCase))
            {
                return true;
            }
        }
    }
}