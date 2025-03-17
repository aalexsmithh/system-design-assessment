import Logo from "./logo";
import VideoTile from "./video-tile";
import { videos } from "./placeholder-data"

export default function Home() {
  return (
    <div>
      <header className="bg-white border-b border-b-gray-200">
        <div className="mx-auto flex h-16  items-center gap-8 px-4 sm:px-6 lg:px-8">
          <a className="block h-8" href="#">
            <Logo />
          </a>

          <div className="flex flex-1 items-center justify-end">
            <div className="flex items-center">
              <div className="sm:flex sm:gap-4">
                <a
                  className="block rounded-md border border-vention-blue bg-vention-blue px-5 py-2.5 text-sm font-medium text-white transition hover:bg-white hover:text-vention-blue"
                  href="#"
                >
                  Login
                </a>
              </div>

            </div>
          </div>
        </div>
      </header>
      <div className="flex flex-row justify-center items-center">
        <div className="grid grid-cols-1 sm:grid-cols-3 sm:max-w-5xl">
          {videos.map((video) => (
            <VideoTile key={video.id} title={video.title} thumbnail={video.thumbnail}/>
          ))}
        </div>
      </div>
      
    </div>

  );
}
