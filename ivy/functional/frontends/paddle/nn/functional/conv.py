import ivy
import ivy.functional.frontends.tensorflow.nn.py as pdf

@to_ivy_arrays_and_back
def conv2D(input, weight, bias, stride, padding, data_format, dilation, name):
  return pdf.conv2D(weight, bias=bias, stride=stride, padding=padding, data_format=data_format, name=name)
