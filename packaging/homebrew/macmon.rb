class Macmon < Formula
  desc "Local system intelligence and observability agent for macOS"
  homepage "https://github.com/yourusername/mac-perf-monitor"
  url "https://github.com/yourusername/mac-perf-monitor/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "REPLACE_WITH_SHA256"
  license "MIT"

  depends_on "python@3.10"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/macmon", "--help"
  end
end
