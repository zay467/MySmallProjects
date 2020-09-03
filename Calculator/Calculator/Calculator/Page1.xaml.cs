using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
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
    /// Interaction logic for Page1.xaml
    /// </summary>
    public partial class Page1 : Page
    {
        public Page1()
        {
            InitializeComponent();
        }
        int pc = 1;
        bool opop = false;
        string op = "";
        double value = 0;
        String data = "";
        List<string> hdata = new List<string>();

        private void zero(object sender, RoutedEventArgs e)
        {
            if (opop)
            {
                tb.Clear();
            }
            opop = false;
            tb.Text += "0";
            data += "0";
            cc();
        }

        private void one(object sender, RoutedEventArgs e)
        {
            if (opop)
            {
                tb.Clear();
            }
            opop = false;
            tb.Text += "1";
            data += "1";
            cc();
        }

        private void two(object sender, RoutedEventArgs e)
        {
            if (opop)
            {
                tb.Clear();
            }
            opop = false;
            tb.Text += "2";
            data += "2";
            cc();
        }

        private void three(object sender, RoutedEventArgs e)
        {
            if (opop)
            {
                tb.Clear();
            }
            opop = false;
            tb.Text += "3";
            data += "3";
            cc();
        }

        private void four(object sender, RoutedEventArgs e)
        {
            if (opop)
            {
                tb.Clear();
            }
            opop = false;
            tb.Text += "4";
            data += "4";
            cc();
        }

        private void five(object sender, RoutedEventArgs e)
        {
            if (opop)
            {
                tb.Clear();
            }
            opop = false;
            tb.Text += "5";
            data += "5";
            cc();
        }

        private void six(object sender, RoutedEventArgs e)
        {
            if (opop)
            {
                tb.Clear();
            }
            opop = false;
            tb.Text += "6";
            data += "6";
            cc();
        }

        private void seven(object sender, RoutedEventArgs e)
        {
            if (opop)
            {
                tb.Clear();
            }
            opop = false;
            tb.Text += "7";
            data += "7";
            cc();
        }

        private void eight(object sender, RoutedEventArgs e)
        {
            if (opop)
            {
                tb.Clear();
            }
            opop = false;
            tb.Text += "8";
            data += "8";
            cc();
        }

        private void nine(object sender, RoutedEventArgs e)
        {
            if (opop)
            {
                tb.Clear();
            }
            opop = false;
            tb.Text += "9";
            data += "9";
            cc();
        }

        private void clear(object sender, RoutedEventArgs e)
        {
            lb.Content = "";
            data = "";
            tb.Clear();
            cc();
        }
        private void dot(object sender, RoutedEventArgs e)
        {
            if (opop)
            {
                tb.Clear();
            }
            opop = false;
            tb.Text += ".";
            data += ".";
            cc();
        }
        private void plus(object sender, RoutedEventArgs e)
        {
            if (pc % 2 != 0)
            {
                op = "+";
                value = Double.Parse(tb.Text);
                opop = true;
                lb.Content = value + " " + op;
                tb.Text = "";
                data += op;
                pc += 1;
            }
            else
            {
                MessageBox.Show("Error", "Information", MessageBoxButton.OK,MessageBoxImage.Error);
            }
        }
        private void minus(object sender, RoutedEventArgs e)
        {
            if (pc % 2 != 0)
            {
                op = "-";
                value = Double.Parse(tb.Text);
                opop = true;
                lb.Content = value + " " + op;
                tb.Text = "";
                data += op;
                pc += 1;
            }
            else
            {
                MessageBox.Show("Error", "Information", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void multiply(object sender, RoutedEventArgs e)
        {
            if (pc % 2 != 0)
            {
                op = "*";
                value = Double.Parse(tb.Text);
                opop = true;
                lb.Content = value + " " + op;
                tb.Text = "";
                data += op;
                pc += 1;
            }
            else
            {
                MessageBox.Show("Error", "Information", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void divide(object sender, RoutedEventArgs e)
        {
            if (pc % 2 != 0)
            {
                op = "/";
                value = Double.Parse(tb.Text);
                opop = true;
                lb.Content = value + " " + op;
                tb.Text = "";
                data += op;
                pc += 1;
            }
            else
            {
                MessageBox.Show("Error", "Information", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        private void modulus(object sender, RoutedEventArgs e)
        {
            if (pc % 2 != 0)
            {
                op = "%";
                value = Double.Parse(tb.Text);
                opop = true;
                lb.Content = value + " " + op;
                tb.Text = "";
                data += op;
                pc += 1;
            }
            else
            {
                MessageBox.Show("Error", "Information", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        private void sqrt(object sender, RoutedEventArgs e)
        {
            if (pc % 2 != 0)
            {
                op = "Sqrt-->";
                value = Double.Parse(tb.Text);
                opop = true;
                lb.Content = op + " " + value;
                tb.Text = Math.Sqrt(value).ToString();
                data += op + tb.Text;
                pc += 0 ;
            }
            else
            {
                MessageBox.Show("Error", "Information", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        private void equal(object sender, RoutedEventArgs e)
        {
            lb.Content = "";
            if (op != "")
            {
                switch (op)
                {
                    case "+":
                        tb.Text = (value + Double.Parse(tb.Text)).ToString();
                        break;
                    case "-":
                        tb.Text = (value - Double.Parse(tb.Text)).ToString();
                        break;
                    case "*":
                        tb.Text = (value * Double.Parse(tb.Text)).ToString();
                        break;
                    case "/":
                        tb.Text = (value / Double.Parse(tb.Text)).ToString();
                        break;
                    case "%":
                        tb.Text = (value + Double.Parse(tb.Text)).ToString();
                        break;
                    default:
                        break;
                }
            }
            data += "=" + tb.Text;
            hdata.Add(data);
            data = "";
        }
        private void history(object sender, RoutedEventArgs e)
        {
            Page2 pg = new Page2(hdata);
            NavigationService.Navigate(pg);
        }
        private void cc()
        {
            pc = 1;
        }
        
    }
}

