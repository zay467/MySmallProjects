using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Collections.Generic;
namespace Calculator
{
    /// <summary>
    /// Interaction logic for Page2.xaml
    /// </summary>
    public partial class Page2 : Page
    {
        List<string> hdata = new List<string>();
        public Page2(List<string> hdata)
        {
            InitializeComponent();
            this.hdata = hdata;
            Grid g = new Grid();
            g.Background = new SolidColorBrush(Colors.Black);
            int mgt = 0;
            foreach(string ss in this.hdata)
            {
                Label lb = new Label();
                lb.Name = "Label";
                lb.Content = ss;
                lb.HorizontalAlignment = HorizontalAlignment.Right;
                lb.FontSize = 20;
                lb.Foreground = new SolidColorBrush(Colors.Orange);
                lb.Margin = new Thickness(0, mgt, 0, 0);
                mgt += 30;
                g.Children.Add(lb);
                
            }
            this.Content = g;
        }
        
    }
}
