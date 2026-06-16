class Causalcore < Formula
  desc "macOS Behavioral Causality Intelligence Engine"
  homepage "https://github.com/CausalCore/mac-perf-monitor"
  url "https://github.com/CausalCore/mac-perf-monitor/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "REPLACE_WITH_SHA256"
  license "MIT"

  depends_on "python@3.9"

  def install
    virtualenv_install_with_resources
    bin.install "venv/bin/causalcore"
  end

  test do
    system "#{bin}/causalcore", "--help"
  end
end
