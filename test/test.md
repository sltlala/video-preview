# 命令行参数

``` rust
// 命令行参数
struct Args {
    /// 处理的文件名
    input_filename: String,

    /// 输出的文件名
    output_filename: Option<String>,

    /// 截图质量
    #[arg(short, long, default_value_t = 4)]
    #[arg(value_parser = clap::value_parser!(u8).range(1..32))]
    // #[arg(value_parser = quality_in_range)]
    quality: u8,

    /// 截图宽高比
    #[arg(short, long, default_value_t = String::from("5:4"))]
    ratio: String,

    /// 是否跳过头尾
    #[arg(short, long, default_value_t = false)]
    anime: bool,

}
```
